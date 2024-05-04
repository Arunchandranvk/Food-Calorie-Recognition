
import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import google.generativeai as genai

load_dotenv()  # Loading environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini-Pro model and predict volume
def predict_volume(image):
    model = genai.GenerativeModel('gemini-pro-vision')
    input_prompt = "You are an expert in nutritionist where you need to see the which is the predicted food and tell only its total weight of the food ."
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileExistsError('No file uploaded')

def create_foodlist():
    list_=['carrot_cake','cheesecake', 'chicken_curry','chicken_wings','club_sandwich',
           'cup_cakes','donuts', 'dumplings', 'french_fries', 'french_onion_soup','fried_rice', 'frozen_yogurt',
           'grilled_cheese_sandwich','hamburger','hummus', 'ice_cream','omelette','pizza','prime_rib','ramen', 
           'red_velvet_cake','samosa','spring_rolls', 'steak', 'waffles']
    return list_
food_cal={
    'carrot_cake': { 'Carbohydrate': 42, 'fat': 17, 'calories': 333, 'protein': 3.8 ,'Ingredients': (' Carrots, flour, sugar, eggs, oil, baking powder, cinnamon, and optionally nuts or raisins.'),'Healthy or Unhealthy': ('Carrot cake is often considered unhealthy due to its high sugar and fat content.')},
    'cheesecake': { 'Carbohydrate': 26, 'fat': 23, 'calories': 321, 'protein': 5.5,'Ingredients': ('Cream cheese, sugar, eggs, and a crust made of crushed cookies or graham crackers.'),'Healthy or Unhealthy':(' Cheesecake is generally considered unhealthy due to its high fat and calorie content.')},
    'chicken_curry': { 'Carbohydrate': 3.2, 'fat': 4.6, 'calories': 104, 'protein': 12,'Ingredients': ('Chicken, curry spices (such as turmeric, cumin, coriander), onions, garlic, ginger, tomatoes, coconut milk or yogurt.') ,'Healthy or Unhealthy':('Chicken curry can be healthy or unhealthy depending on the recipe and ingredients used. It can be nutritious if prepared with lean protein, vegetables, and minimal added fats.')},
    'chicken_wings': { 'Carbohydrate': 9.8, 'fat': 24, 'calories': 328, 'protein': 17,'Ingredients': (' Chicken wings, oil for frying, and sauce (which can vary but often includes butter and hot sauce).'),'Healthy or Unhealthy':('Chicken wings are typically considered unhealthy due to their high fat and calorie content, especially if they are fried and coated in sauce.') },
    'club_sandwich': { 'Carbohydrate': 12, 'fat': 13, 'calories': 234, 'protein': 16,'Ingredients': ('Turkey or chicken slices, bacon, lettuce, tomato, mayonnaise, bread (usually three slices.)'),'Healthy or Unhealthy':('A club sandwich can be made healthier by choosing whole grain bread and lean protein, but it can also be unhealthy if it contains high-fat ingredients like bacon and mayonnaise.')},
    'cup_cakes': { 'Carbohydrate': 40, 'fat': 15, 'calories': 292, 'protein': 2.6,'Ingredients': ('Flour, sugar, eggs, butter or oil, baking powder, and flavorings (such as vanilla extract). Frosting typically contains powdered sugar and butter or cream cheese.') ,'Healthy or Unhealthy':('Cupcakes are generally considered unhealthy due to their high sugar and fat content, especially if they are frosted.')},
    'donuts': { 'Carbohydrate': 29, 'fat': 14, 'calories': 253, 'protein': 3.7 ,'Ingredients': (' Flour, sugar, eggs, yeast or baking powder, milk, and oil for frying. Glaze or icing is often added on top.'),'Healthy or Unhealthy':('Donuts are typically considered unhealthy due to their high sugar and fat content, especially if they are fried.')},
    'dumplings': { 'Carbohydrate': 12, 'fat': 1.7, 'calories': 74, 'protein': 2 ,'Ingredients': ('Dumpling wrappers made of flour and water, and fillings such as ground meat, vegetables, or seafood.'),'Healthy or Unhealthy':('Dumplings can be healthy or unhealthy depending on their ingredients and how they are prepared. Steamed or boiled dumplings with lean fillings like vegetables or shrimp are healthier than fried dumplings with fatty fillings like pork.')},
    'omelette': { 'Carbohydrate': 0.6, 'fat': 12, 'calories': 154, 'protein': 11,'Ingredients': ('Eggs, vegetables (such as bell peppers, onions, spinach, and mushrooms), cheese, and seasonings.'),'Healthy or Unhealthy':('Omelettes can be healthy or unhealthy depending on the ingredients used. Adding plenty of vegetables and using minimal cheese can make them a nutritious choice.') },
    'pizza': { 'Carbohydrate': 26, 'fat': 10.1, 'calories': 237, 'protein': 10.6,'Ingredients': ('Pizza dough or crust, tomato sauce, cheese (such as mozzarella), and various toppings (such as pepperoni, mushrooms, onions, and bell peppers).') ,'Healthy or Unhealthy':('Pizza can vary widely in its nutritional content depending on the crust, cheese, and toppings. Opting for a thin crust and loading up on vegetables can make it a healthier option.')},
    'prime_rib': { 'Carbohydrate': 0, 'fat': 7.27, 'calories': 112, 'protein': 10.88,'Ingredients': ('Prime rib roast (bone-in or boneless), seasonings (such as salt, pepper, and herbs).') ,'Healthy or Unhealthy':('Prime rib is a rich and flavorful cut of beef that is high in fat and calories. It is typically considered a special occasion or indulgent meal rather than a regular part of a healthy diet.')},
    'red_velvet_cake': { 'Carbohydrate': 37.45, 'fat': 13.74, 'calories': 293, 'protein': 5.45,'Ingredients': ('Flour, cocoa powder, buttermilk, butter, sugar, eggs, red food coloring, vinegar, baking soda, cream cheese, powdered sugar.') ,'Healthy or Unhealthy':('Flour, cocoa powder, buttermilk, butter, sugar, eggs, red food coloring, vinegar, baking soda, cream cheese, powdered sugar.')},
    'samosa': { 'Carbohydrate': 21, 'fat': 10, 'calories': 190, 'protein': 4 ,'Ingredients': ('Pastry dough (made from flour, water, and sometimes oil), potato, peas, carrots, onions, spices (such as cumin, coriander, and garam masala).'),'Healthy or Unhealthy':('Samosas are often fried, making them high in calories and fat. However, baked versions are available for a healthier option. The filling typically consists of vegetables, potatoes, and sometimes meat or lentils.')},
    'spring_rolls': { 'Carbohydrate': 13, 'fat': 5, 'calories': 110, 'protein': 3 ,'Ingredients': (' Rice paper wrappers, vermicelli noodles, lettuce, shrimp or chicken, mint, cilantro, and dipping sauce.'),'Healthy or Unhealthy':('Spring rolls can be healthy or unhealthy depending on whether they are fried or fresh. Fresh spring rolls made with rice paper and filled with vegetables and lean protein are a lighter option compared to fried spring rolls.')},
    'steak': { 'Carbohydrate': 0, 'fat': 14.84, 'calories': 251, 'protein': 27.4 ,'Ingredients': (' Beef steak (such as ribeye, sirloin, or filet mignon), salt, pepper, and optional seasonings or marinades.'),'Healthy or Unhealthy':('Steak is a good source of protein and essential nutrients like iron and zinc. However, it can be high in saturated fat, so its essential to choose lean cuts and moderate portion sizes.')},
    'waffles': { 'Carbohydrate': 26.60, 'fat': 12.1, 'calories': 241, 'protein': 5.7 ,'Ingredients': ('Waffle batter (made from flour, eggs, milk, and oil or butter), syrup, butter, and toppings (such as fruit, whipped cream, or chocolate chips).'),'Healthy or Unhealthy':(' Waffles can be healthy or unhealthy depending on the ingredients used and toppings added. Opting for whole grain waffles and topping them with fresh fruit and a modest amount of syrup can make them a nutritious choice.')},
    'french_fries': { 'Carbohydrate': 41, 'fat': 15, 'calories': 312, 'protein': 3.4 ,'Ingredients': ('Potatoes, oil for frying, and salt. Additional seasonings or toppings may be added, such as garlic, herbs, or cheese.'),'Healthy or Unhealthy':('French fries are generally considered unhealthy due to their high fat and calorie content, especially when deep-fried.')},
    'french_onion_soup': { 'Carbohydrate': 11, 'fat': 6.8, 'calories': 137, 'protein': 6 ,'Ingredients': ('Onions, beef or vegetable broth, butter, white wine, and optionally bread and cheese for topping.'),'Healthy or Unhealthy':('French onion soup can be healthy or unhealthy depending on the recipe. Its typically lower in calories if its made with a light broth and served without excessive cheese or bread.')},
    'fried_rice': { 'Carbohydrate': 33, 'fat': 3, 'calories': 174, 'protein': 4.1,'Ingredients': (' Cooked rice, vegetables (such as peas, carrots, and onions), eggs, soy sauce, and protein (such as chicken, shrimp, or tofu).') ,'Healthy or Unhealthy':('Fried rice can be healthy or unhealthy depending on the ingredients and cooking methods used. It can be made healthier by using brown rice and adding plenty of vegetables and lean protein.')},
    'frozen_yogurt': { 'Carbohydrate': 22, 'fat': 3.6, 'calories': 127, 'protein': 3,'Ingredients': ('Yogurt, sugar or sweeteners, and flavorings. Fruit purees or extracts are often used for flavoring.'),'Healthy or Unhealthy':('Frozen yogurt is often considered healthier than ice cream because it typically contains less fat. However, it can still be high in sugar, depending on the flavor and toppings.') },
    'grilled_cheese_sandwich': { 'Carbohydrate': 27, 'fat': 22, 'calories': 344, 'protein': 11,'Ingredients': ('Bread, cheese (such as cheddar or American), and butter or margarine.') ,'Healthy or Unhealthy':('Grilled cheese sandwiches can be relatively high in calories and fat, especially if they are made with a lot of cheese and butter. Using whole grain bread and reducing the amount of cheese and butter can make them healthier.')},
    'hamburger': { 'Carbohydrate': 18, 'fat': 12, 'calories': 239, 'protein': 15,'Ingredients': ('Ground beef or turkey, hamburger buns, lettuce, tomato, onion, cheese, ketchup, mustard, and mayonnaise.'),'Healthy or Unhealthy':('Hamburgers can vary widely in their nutritional content depending on the type of meat, toppings, and portion size. Lean ground beef or turkey burgers served with plenty of vegetables can be a healthier option compared to larger burgers with lots of cheese and mayonnaise.') },
    'hummus': { 'Carbohydrate': 14, 'fat': 9.6, 'calories': 166, 'protein': 7.9 ,'Ingredients': ('Chickpeas (garbanzo beans), tahini (sesame seed paste), olive oil, lemon juice, garlic, and salt.'),'Healthy or Unhealthy':('Hummus is generally considered healthy as it is made from chickpeas, which are high in protein and fiber. However, store-bought varieties may contain added oils and preservatives, so its essential to check the ingredients.')},
    'ice_cream': { 'Carbohydrate': 24, 'fat': 11, 'calories': 207, 'protein': 3.5 ,'Ingredients': ('Milk or cream, sugar, flavorings (such as vanilla or chocolate), and sometimes eggs or egg yolks.'),'Healthy or Unhealthy':('ce cream is often high in sugar and fat, making it a less healthy option when consumed in large amounts. However, there are lighter versions available that use lower-fat milk and less sugar.')},
    'ramen': { 'Carbohydrate': 26, 'fat': 7, 'calories': 26, 'protein': 4 ,'Ingredients': ('Ramen noodles, broth (such as miso, soy sauce, or tonkotsu), toppings (such as sliced pork, soft-boiled egg, green onions, and nori).'),'Healthy or Unhealthy':('Ramen can vary widely in its nutritional content depending on the broth, noodles, and toppings. Instant ramen noodles are often high in sodium and low in nutrients, while homemade or restaurant versions can be made healthier with added vegetables and lean protein.')}
}


def predict_class(model, img):
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.

    pred = model.predict(img)
    index = np.argmax(pred)
    val = np.amax(pred)
    pred_value = food_list[index]

    if val < 0.2:
        pred_value = "Not a food item !"
        return pred_value, None
    else:
        return pred_value, food_cal.get(pred_value, None)

# Initialize our streamlit app
def main():
    st.set_page_config(page_title="Food Recognition App")
    st.header("Food Recognition App")
    uploaded_file = st.file_uploader("Upload an image...", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        model = load_model('D:/Internship Luminar/Main Projects/Image Food Recognition/food_recognition.h5', compile=False)
        img = image.load_img(uploaded_file, target_size=(228,228))
        st.image(img, caption='Uploaded Image', use_column_width=True)
        pred_value, cal_data = predict_class(model, img)
    
    submit = st.button("Details about the Food")  
    if submit:
        if cal_data is not None:
            st.write("Predicted Food:", pred_value)
            st.write("Nutrition Information:")
            for key, value in cal_data.items():
                st.write(f"{key}: {value}")
            if uploaded_file is not None:
                image_data = input_image_setup(uploaded_file)
                predicted_volume = predict_volume(image_data)
                st.write("Predicted Volume:", predicted_volume)
        else:
            st.write("Not a food item!")

if __name__ == "__main__":
    food_list = create_foodlist()
    main()











































# import streamlit as st
# from tensorflow.keras.preprocessing import image
# import numpy as np
# from tensorflow.keras.models import load_model


# def create_foodlist():
#     list_=['carrot_cake','cheesecake', 'chicken_curry','chicken_wings','club_sandwich',
#            'cup_cakes','donuts', 'dumplings', 'french_fries', 'french_onion_soup','fried_rice', 'frozen_yogurt',
#            'grilled_cheese_sandwich','hamburger','hummus', 'ice_cream','omelette','pizza','prime_rib','ramen', 
#            'red_velvet_cake','samosa','spring_rolls', 'steak', 'waffles']
#     return list_
# food_cal={
#     'carrot_cake': { 'Carbohydrate': 42, 'fat': 17, 'calories': 333, 'protein': 3.8 ,'Ingredients': (' Carrots, flour, sugar, eggs, oil, baking powder, cinnamon, and optionally nuts or raisins.'),'Healthy or Unhealthy': ('Carrot cake is often considered unhealthy due to its high sugar and fat content.')},
#     'cheesecake': { 'Carbohydrate': 26, 'fat': 23, 'calories': 321, 'protein': 5.5,'Ingredients': ('Cream cheese, sugar, eggs, and a crust made of crushed cookies or graham crackers.'),'Healthy or Unhealthy':(' Cheesecake is generally considered unhealthy due to its high fat and calorie content.')},
#     'chicken_curry': { 'Carbohydrate': 3.2, 'fat': 4.6, 'calories': 104, 'protein': 12,'Ingredients': ('Chicken, curry spices (such as turmeric, cumin, coriander), onions, garlic, ginger, tomatoes, coconut milk or yogurt.') ,'Healthy or Unhealthy':('Chicken curry can be healthy or unhealthy depending on the recipe and ingredients used. It can be nutritious if prepared with lean protein, vegetables, and minimal added fats.')},
#     'chicken_wings': { 'Carbohydrate': 9.8, 'fat': 24, 'calories': 328, 'protein': 17,'Ingredients': (' Chicken wings, oil for frying, and sauce (which can vary but often includes butter and hot sauce).'),'Healthy or Unhealthy':('Chicken wings are typically considered unhealthy due to their high fat and calorie content, especially if they are fried and coated in sauce.') },
#     'club_sandwich': { 'Carbohydrate': 12, 'fat': 13, 'calories': 234, 'protein': 16,'Ingredients': ('Turkey or chicken slices, bacon, lettuce, tomato, mayonnaise, bread (usually three slices.)'),'Healthy or Unhealthy':('A club sandwich can be made healthier by choosing whole grain bread and lean protein, but it can also be unhealthy if it contains high-fat ingredients like bacon and mayonnaise.')},
#     'cup_cakes': { 'Carbohydrate': 40, 'fat': 15, 'calories': 292, 'protein': 2.6,'Ingredients': ('Flour, sugar, eggs, butter or oil, baking powder, and flavorings (such as vanilla extract). Frosting typically contains powdered sugar and butter or cream cheese.') ,'Healthy or Unhealthy':('Cupcakes are generally considered unhealthy due to their high sugar and fat content, especially if they are frosted.')},
#     'donuts': { 'Carbohydrate': 29, 'fat': 14, 'calories': 253, 'protein': 3.7 ,'Ingredients': (' Flour, sugar, eggs, yeast or baking powder, milk, and oil for frying. Glaze or icing is often added on top.'),'Healthy or Unhealthy':('Donuts are typically considered unhealthy due to their high sugar and fat content, especially if they are fried.')},
#     'dumplings': { 'Carbohydrate': 12, 'fat': 1.7, 'calories': 74, 'protein': 2 ,'Ingredients': ('Dumpling wrappers made of flour and water, and fillings such as ground meat, vegetables, or seafood.'),'Healthy or Unhealthy':('Dumplings can be healthy or unhealthy depending on their ingredients and how they are prepared. Steamed or boiled dumplings with lean fillings like vegetables or shrimp are healthier than fried dumplings with fatty fillings like pork.')},
#     'omelette': { 'Carbohydrate': 0.6, 'fat': 12, 'calories': 154, 'protein': 11,'Ingredients': ('Eggs, vegetables (such as bell peppers, onions, spinach, and mushrooms), cheese, and seasonings.'),'Healthy or Unhealthy':('Omelettes can be healthy or unhealthy depending on the ingredients used. Adding plenty of vegetables and using minimal cheese can make them a nutritious choice.') },
#     'pizza': { 'Carbohydrate': 26, 'fat': 10.1, 'calories': 237, 'protein': 10.6,'Ingredients': ('Pizza dough or crust, tomato sauce, cheese (such as mozzarella), and various toppings (such as pepperoni, mushrooms, onions, and bell peppers).') ,'Healthy or Unhealthy':('Pizza can vary widely in its nutritional content depending on the crust, cheese, and toppings. Opting for a thin crust and loading up on vegetables can make it a healthier option.')},
#     'prime_rib': { 'Carbohydrate': 0, 'fat': 7.27, 'calories': 112, 'protein': 10.88,'Ingredients': ('Prime rib roast (bone-in or boneless), seasonings (such as salt, pepper, and herbs).') ,'Healthy or Unhealthy':('Prime rib is a rich and flavorful cut of beef that is high in fat and calories. It is typically considered a special occasion or indulgent meal rather than a regular part of a healthy diet.')},
#     'red_velvet_cake': { 'Carbohydrate': 37.45, 'fat': 13.74, 'calories': 293, 'protein': 5.45,'Ingredients': ('Flour, cocoa powder, buttermilk, butter, sugar, eggs, red food coloring, vinegar, baking soda, cream cheese, powdered sugar.') ,'Healthy or Unhealthy':('Flour, cocoa powder, buttermilk, butter, sugar, eggs, red food coloring, vinegar, baking soda, cream cheese, powdered sugar.')},
#     'samosa': { 'Carbohydrate': 21, 'fat': 10, 'calories': 190, 'protein': 4 ,'Ingredients': ('Pastry dough (made from flour, water, and sometimes oil), potato, peas, carrots, onions, spices (such as cumin, coriander, and garam masala).'),'Healthy or Unhealthy':('Samosas are often fried, making them high in calories and fat. However, baked versions are available for a healthier option. The filling typically consists of vegetables, potatoes, and sometimes meat or lentils.')},
#     'spring_rolls': { 'Carbohydrate': 13, 'fat': 5, 'calories': 110, 'protein': 3 ,'Ingredients': (' Rice paper wrappers, vermicelli noodles, lettuce, shrimp or chicken, mint, cilantro, and dipping sauce.'),'Healthy or Unhealthy':('Spring rolls can be healthy or unhealthy depending on whether they are fried or fresh. Fresh spring rolls made with rice paper and filled with vegetables and lean protein are a lighter option compared to fried spring rolls.')},
#     'steak': { 'Carbohydrate': 0, 'fat': 14.84, 'calories': 251, 'protein': 27.4 ,'Ingredients': (' Beef steak (such as ribeye, sirloin, or filet mignon), salt, pepper, and optional seasonings or marinades.'),'Healthy or Unhealthy':('Steak is a good source of protein and essential nutrients like iron and zinc. However, it can be high in saturated fat, so its essential to choose lean cuts and moderate portion sizes.')},
#     'waffles': { 'Carbohydrate': 26.60, 'fat': 12.1, 'calories': 241, 'protein': 5.7 ,'Ingredients': ('Waffle batter (made from flour, eggs, milk, and oil or butter), syrup, butter, and toppings (such as fruit, whipped cream, or chocolate chips).'),'Healthy or Unhealthy':(' Waffles can be healthy or unhealthy depending on the ingredients used and toppings added. Opting for whole grain waffles and topping them with fresh fruit and a modest amount of syrup can make them a nutritious choice.')},
#     'french_fries': { 'Carbohydrate': 41, 'fat': 15, 'calories': 312, 'protein': 3.4 ,'Ingredients': ('Potatoes, oil for frying, and salt. Additional seasonings or toppings may be added, such as garlic, herbs, or cheese.'),'Healthy or Unhealthy':('French fries are generally considered unhealthy due to their high fat and calorie content, especially when deep-fried.')},
#     'french_onion_soup': { 'Carbohydrate': 11, 'fat': 6.8, 'calories': 137, 'protein': 6 ,'Ingredients': ('Onions, beef or vegetable broth, butter, white wine, and optionally bread and cheese for topping.'),'Healthy or Unhealthy':('French onion soup can be healthy or unhealthy depending on the recipe. Its typically lower in calories if its made with a light broth and served without excessive cheese or bread.')},
#     'fried_rice': { 'Carbohydrate': 33, 'fat': 3, 'calories': 174, 'protein': 4.1,'Ingredients': (' Cooked rice, vegetables (such as peas, carrots, and onions), eggs, soy sauce, and protein (such as chicken, shrimp, or tofu).') ,'Healthy or Unhealthy':('Fried rice can be healthy or unhealthy depending on the ingredients and cooking methods used. It can be made healthier by using brown rice and adding plenty of vegetables and lean protein.')},
#     'frozen_yogurt': { 'Carbohydrate': 22, 'fat': 3.6, 'calories': 127, 'protein': 3,'Ingredients': ('Yogurt, sugar or sweeteners, and flavorings. Fruit purees or extracts are often used for flavoring.'),'Healthy or Unhealthy':('Frozen yogurt is often considered healthier than ice cream because it typically contains less fat. However, it can still be high in sugar, depending on the flavor and toppings.') },
#     'grilled_cheese_sandwich': { 'Carbohydrate': 27, 'fat': 22, 'calories': 344, 'protein': 11,'Ingredients': ('Bread, cheese (such as cheddar or American), and butter or margarine.') ,'Healthy or Unhealthy':('Grilled cheese sandwiches can be relatively high in calories and fat, especially if they are made with a lot of cheese and butter. Using whole grain bread and reducing the amount of cheese and butter can make them healthier.')},
#     'hamburger': { 'Carbohydrate': 18, 'fat': 12, 'calories': 239, 'protein': 15,'Ingredients': ('Ground beef or turkey, hamburger buns, lettuce, tomato, onion, cheese, ketchup, mustard, and mayonnaise.'),'Healthy or Unhealthy':('Hamburgers can vary widely in their nutritional content depending on the type of meat, toppings, and portion size. Lean ground beef or turkey burgers served with plenty of vegetables can be a healthier option compared to larger burgers with lots of cheese and mayonnaise.') },
#     'hummus': { 'Carbohydrate': 14, 'fat': 9.6, 'calories': 166, 'protein': 7.9 ,'Ingredients': ('Chickpeas (garbanzo beans), tahini (sesame seed paste), olive oil, lemon juice, garlic, and salt.'),'Healthy or Unhealthy':('Hummus is generally considered healthy as it is made from chickpeas, which are high in protein and fiber. However, store-bought varieties may contain added oils and preservatives, so its essential to check the ingredients.')},
#     'ice_cream': { 'Carbohydrate': 24, 'fat': 11, 'calories': 207, 'protein': 3.5 ,'Ingredients': ('Milk or cream, sugar, flavorings (such as vanilla or chocolate), and sometimes eggs or egg yolks.'),'Healthy or Unhealthy':('ce cream is often high in sugar and fat, making it a less healthy option when consumed in large amounts. However, there are lighter versions available that use lower-fat milk and less sugar.')},
#     'ramen': { 'Carbohydrate': 26, 'fat': 7, 'calories': 26, 'protein': 4 ,'Ingredients': ('Ramen noodles, broth (such as miso, soy sauce, or tonkotsu), toppings (such as sliced pork, soft-boiled egg, green onions, and nori).'),'Healthy or Unhealthy':('Ramen can vary widely in its nutritional content depending on the broth, noodles, and toppings. Instant ramen noodles are often high in sodium and low in nutrients, while homemade or restaurant versions can be made healthier with added vegetables and lean protein.')}
# }

# def predict_class(model, img):
#     img = image.img_to_array(img)
#     img = np.expand_dims(img, axis=0)
#     img /= 255.

#     pred = model.predict(img)
#     index = np.argmax(pred)
#     val = np.amax(pred)
#     pred_value = food_list[index]

#     if val < 0.2:
#         pred_value = "Not a food item !"
#         return pred_value, None
#     else:
#         return pred_value, food_cal.get(pred_value, None)
# #initialize our streamlit app
# def main():
#     st.set_page_config(page_title="food recognition App")
#     st.header("food recognition App")
#     uploaded_file = st.file_uploader("Upload an image...", type=["png", "jpg", "jpeg"])
    

#     if uploaded_file is not None:
#         model = load_model('/home/niyas/Downloads/food_recognition.h5', compile=False)
#         img = image.load_img(uploaded_file, target_size=(228,228))
#         st.image(img, caption='Uploaded Image', use_column_width=True)
#         pred_value, cal_data = predict_class(model, img)
#     submit=st.button("Details about the Food")  
#     if submit:
#         if cal_data is not None:
#             st.write("Predicted Food:", pred_value)
#             st.write("Nutrition Information:", cal_data)
#         else:
#             st.write("Not a food item!")

# if __name__ == "__main__":
#     food_list = create_foodlist()
#     main()


