import streamlit as st
import streamlit.components.v1 as components
import requests
import os
import time

st.set_page_config(
    page_title="Getaround Project",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
  )


st.header("Try Out the API by Picking From the Options Below:")

col_1,col_2,col_3,col_4,col_5,col_6,col_7 = st.columns(7)

def yes_no_none(yesno):
	match yesno:
		case "Yes":
			return True
		case "No":
			return False
		case _:
			return None

with col_1:

	model_key_options: list[str] = ["Citroën", "Renault", "BMW", "Peugeot", "Audi", "Nissan", "Mitsubishi",
                                  "Mercedes", "Volkswagen", "Toyota", "SEAT", "Subaru", "PGO", "Ferrari",
                                  "Opel", "Maserati", "Suzuki", "Porsche", "Ford", "KIA Motors", "Alfa Romeo",
                                  "Fiat", "Lexus", "Lamborghini", "Mazda", "Honda", "Mini", "Yamaha", "Pick one"] # the default input prompt text gets truncated, so I made a shorter one
	model_key_input = st.selectbox("Make",
									model_key_options,
									index=len(model_key_options)-1) # -1 by itself is not a valid index here

	mileage_input = st.number_input("Mileage",
									step=1,
									min_value=0, 
									value=0) # Unsure what the units are

with col_2:

	engine_power_input = st.number_input("Engine power",
										step=1,
										min_value=0,
										value=0) # Unsure what the unit is

	fuel_options_dict = {"Diesel": "diesel", "Petrol": "petrol", "Hybrid": "hybrid_petrol", "Electric": "electro", "Pick one": "Pick one"}
	fuel_input_from_options = st.selectbox("Fuel",
											list(fuel_options_dict.keys()),
											index=len(fuel_options_dict)-1)
	fuel_input_formatted: str = fuel_options_dict[fuel_input_from_options]

with col_3:

	paint_color_options_dict = {"Black": "black", "Grey": "grey", "Blue": "blue", "White": "white", "Brown": "brown", "Silver": "silver",
							 	"Red": "red", "Beige": "beige", "Green": "green", "Orange": "orange", "Pick one": "Pick one"}
	paint_color_input_from_options = st.selectbox("Paint colour",
											list(paint_color_options_dict.keys()),
											index=len(paint_color_options_dict)-1)
	paint_color_input_formatted:str = paint_color_options_dict[paint_color_input_from_options]

	car_type_options_dict = {"Estate": "estate","Sedan": "sedan", "SUV": "suv", "Hatchback": "hatchback",
                           	 "Subcompact": "subcompact", "Coupé": "coupe", "Convertible": "convertible", "Van": "van", "Pick one": "Pick one"}
	car_type_input_from_options = st.selectbox("Car type",
												list(car_type_options_dict.keys()),
												index=len(car_type_options_dict)-1)
	car_type_input_formatted: str = car_type_options_dict[car_type_input_from_options]

with col_4:

	private_parking_available_options = ["Yes", "No", "Pick one"]
	private_parking_available_input_yesno = st.selectbox("Private parking available",
														private_parking_available_options,
														index=len(private_parking_available_options)-1)
	private_parking_available_input_bool: bool|None = yes_no_none(private_parking_available_input_yesno)

	has_gps_options = ["Yes", "No", "Pick one"]
	has_gps_input_yesno = st.selectbox("Has a GPS",
										has_gps_options,
										index=len(has_gps_options)-1)
	has_gps_input_bool: bool|None = yes_no_none(has_gps_input_yesno)

with col_5:

	has_air_conditioning_options = ["Yes", "No", "Pick one"]
	has_air_conditioning_input_yesno = st.selectbox("Has air conditioning",
													has_air_conditioning_options,
													index=len(has_air_conditioning_options)-1)
	has_air_conditioning_input_bool: bool|None = yes_no_none(has_air_conditioning_input_yesno)

	automatic_car_options = ["Yes", "No", "Pick one"]
	automatic_car_input_yesno = st.selectbox("Has an automatic gearbox",
											automatic_car_options,
											index=len(automatic_car_options)-1)
	automatic_car_input_bool: bool|None = yes_no_none(automatic_car_input_yesno)

with col_6:

	has_getaround_connect_options = ["Yes", "No", "Pick one"]
	has_getaround_connect_input_yesno = st.selectbox("Has Getaround Connect",
													has_getaround_connect_options,
													index=len(has_getaround_connect_options)-1)
	has_getaround_connect_input_bool: bool|None = yes_no_none(has_getaround_connect_input_yesno)

	has_speed_regulator_options = ["Yes", "No", "Pick one"]
	has_speed_regulator_input_yesno = st.selectbox("Has a speed regulator",
													has_speed_regulator_options,
													index=len(has_speed_regulator_options)-1)
	has_speed_regulator_input_bool: bool|None = yes_no_none(has_speed_regulator_input_yesno)

with col_7:

	winter_tires_options = ["Yes", "No", "Pick one"]
	winter_tires_input_yesno = st.selectbox("Has winter tyres",
											winter_tires_options,
											index=len(winter_tires_options)-1)
	winter_tires_input_bool: bool|None = yes_no_none(winter_tires_input_yesno)
	

api_url = os.environ["PRICE_API_URL"]

@st.cache_data(show_spinner=False)
def call_price_api(inputs):
	try:
		response = requests.post(url=f"{api_url}/predict", json=dict(CarActeristics=inputs))
		st.markdown(f"The estimated daily rental price of the vehicle is €{response.json()["prediction"]:.2f}")
	except Exception as e:
		print(f"Something went wrong when calling the API. Trying again in 5 seconds.\n{e}")
		time.sleep(5)
		call_price_api(inputs)

inputs_list = [model_key_input, mileage_input, engine_power_input, fuel_input_formatted, paint_color_input_formatted,
               car_type_input_formatted, private_parking_available_input_bool, has_gps_input_bool, has_air_conditioning_input_bool,
               automatic_car_input_bool, has_getaround_connect_input_bool, has_speed_regulator_input_bool, winter_tires_input_bool]		

_, button_col, _ = st.columns(3)
if button_col.button("Call the API", width="stretch"):
	if ("Pick one" not in inputs_list) and (None not in inputs_list):
		with st.spinner("Fetching the results..."):
			call_price_api([inputs_list]) # the API takes a list of lists
	else:
		st.markdown("Oops! It seems that at least one of the options was skipped.")
	   


with st.expander("API documentation"):
	components.iframe(f"{api_url}/docs#/", height=3000)