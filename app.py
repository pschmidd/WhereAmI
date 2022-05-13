import tkintermapview
import pandas as pd
from geopy import distance
from tkinter import *

cities = pd.read_csv('data/cities.csv', delimiter=',')
borders = pd.read_csv('data/borders.csv', delimiter=',')
bord = borders[["sovereignt", "coordinates"]]


class App(Tk):
    def __init__(self):
        super().__init__()

        map_widget = tkintermapview.TkinterMapView(self, width=1200, height=900, corner_radius=0)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        map_widget.set_zoom(1)
        map_widget.place(x=900, y=450, anchor='center')
        polygon_list = map_widget.canvas_polygon_list
        marker_list = map_widget.canvas_marker_list
        coordinates_list = []
        city_list = []

        def show_hint():
            lbl_country.configure(background='SystemButtonFace')

            country_to_find = bord.loc[bord["sovereignt"] == str_country.get()]
            border = list(country_to_find["coordinates"])
            border = "".join(border)

            border = border.split(",")

            res = [(float(j), float(i)) for i, j in zip(border[::2], border[1::2])]

            country_border = map_widget.set_polygon(
                res,
                border_width=0.5,
                fill_color="red"
            )
            polygon_list.append(country_border)

        def rnd_place():
            coordinates_list.clear()
            city_list.clear()
            if len(polygon_list) > 0:
                for item in polygon_list:
                    item.delete()
            random_place = cities.sample(n=1)
            lat = random_place['lat'].loc[random_place.index[0]]
            lng = random_place['lng'].loc[random_place.index[0]]
            city = random_place['city'].loc[random_place.index[0]]
            country = random_place['country'].loc[random_place.index[0]]
            coord1 = (lat, lng)
            str_find_me.set(city)
            str_country.set(country)
            lbl_country.configure(background='black')
            coordinates_list.append(coord1)
            city_list.append(city)

        def add_marker_event(coords):
            player_marker = map_widget.set_marker(coords[0], coords[1], text="Marker Player 1")
            p_lat = coords[0]
            p_lng = coords[1]
            coord2 = (p_lat, p_lng)
            coordinates_list.append(coord2)

        def show_path():
            map_widget.set_position(coordinates_list[0][0], coordinates_list[0][1], marker=True, text=city_list[0])
            map_widget.set_zoom(3)
            path = map_widget.set_path([coordinates_list[0], coordinates_list[1]])
            dist = distance.distance(coordinates_list[0], coordinates_list[1]).km
            str_distance.set(str(round(dist, 2)) + " km")
            points = float(round(3000 - dist, 2))
            str_points.set(str(points) + " Punkte")
            lb_points.insert('end', points)
            if lb_hiscore.size() < 1:
                lb_hiscore.insert('end', points)
            else:
                points_kum = lb_hiscore.get('end')
                high = round(float(points_kum) + float(points), 2)
                lb_hiscore.delete(0, 'end')
                lb_hiscore.insert('end', high)

        map_widget.add_right_click_menu_command(label="Add Marker",
                                                command=add_marker_event,
                                                pass_coords=True)
        # select city to be found
        btn_rnd_place = Button(
            self,
            text="find me",
            command=rnd_place
        )
        btn_rnd_place.place(x=10, y=10)
        # get distance
        btn_path = Button(
            self,
            text="distance",
            command=show_path
        )
        btn_path.place(x=10, y=50)
        # get hint
        btn_hint = Button(
            self,
            text="need a hint?",
            command=show_hint
        )
        btn_hint.place(x=80, y=10)
        # distance
        str_distance = StringVar()
        str_distance.set("distance in km")

        lbl_distance = Label(
            self,
            textvariable=str_distance,
            font=('Courir', 25)
        )
        lbl_distance.place(x=10, y=200)
        # city
        str_find_me = StringVar()
        str_find_me.set("find me")

        lbl_find_me = Label(
            self,
            textvariable=str_find_me,
            font=('Courir', 15)
        )
        lbl_find_me.place(x=10, y=105)
        # country
        str_country = StringVar()
        str_country.set("find me")

        lbl_country = Label(
            self,
            textvariable=str_country,
            font=('Courir', 15),
            background="black"
        )
        lbl_country.place(x=10, y=150)
        # points
        str_points = StringVar()
        str_points.set("your points")

        lbl_points = Label(
            self,
            textvariable=str_points,
            font=('Courir', 15)
        )
        lbl_points.place(x=10, y=250)
        # listbox points
        lb_points = Listbox(
            self,
            font=('Courir', 15)
        )
        lb_points.place(x=10, y=300)
        # listbox hiscore
        lb_hiscore = Listbox(
            self,
            font=('Courir', 15)
        )
        lb_hiscore.place(x=10, y=550)


if __name__ == "__main__":
    app = App()
    app.title('Where Am I?')
    app.geometry('1500x900')
    app.resizable(False, False)
    app.mainloop()