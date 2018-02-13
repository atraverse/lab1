import folium
import geocoder


def read_file(path):
    '''
    (str)->(list)
    Return list of file's lines
    '''
    lst = []
    with open(path) as f:
        for line in f:
            lst.append(line)
    for i in range(14):
        del lst[0]
    return lst


def find_year(lst, year):
    '''
    (list, str)->(list)
    Return list with information for the specified year
    '''
    lst_f = [i for i in lst if year in i]
    return (lst_f)


def lst_loc(lst):
    '''
    (list)->(list)
    Modified list, leave only location, but delete else
    '''
    lst_loc = ["".join(i.split()[-3:]) for i  in lst]
    return (lst_loc)


def coordinates(lst_loc):
    '''
    (list)->(list)
    Return list with coordinates
    '''
    lst = []
    for i in lst_loc:
        try:
            g = geocoder.google(i)
            g1 = g.latlng
            lst.append(g1)
        except:
            pass
    return lst


def create_html():
    '''
    Main function, create HTML file and enter information to it
    '''
    year = str(input("Year: "))
    lst_year = find_year(read_file('list.txt'),year)
    loc = lst_loc(lst_year)
    lst = coordinates(loc)
    map1 = folium.Map(location =lst[0], zoom_start = 4)
    films = folium.FeatureGroup(name='Films')
    for i in lst:
        films.add_child(folium.Marker(location=i, icon=folium.Icon()))
    population = folium.FeatureGroup(name="Population")
    population.add_child(folium.GeoJson(data=open('world.json', 'r', \
                                        encoding='utf-8-sig').read(),
                                        style_function=lambda x: {
                                            'fillColor': 'green'
                                            if x['properties'][
                                                   'POP2005'] < 10000000
                                            else 'orange' if 10000000 <=
                                                          x['properties'][
                                                              'POP2005'] < 20000000
                                            else 'red'}))

    map1.add_child(films)
    map1.add_child(population)
    map1.add_child(folium.LayerControl())
    map1.save('result.html')
create_html()
