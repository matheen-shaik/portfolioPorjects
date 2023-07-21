import pandas as pd
import requests

class InvalidTypeException(Exception):
    pass

class InvalidCoreException(Exception):
    pass


class IndianFoodRecommendation:
    def __init__(self):
        self.df = self.load_data()
        #print(self.df) 

    def load_data(self):
        url = "https://ind-nutrient-api1.p.rapidapi.com/food/core"

        headers = {
            "X-RapidAPI-Key": "5414589f59msha714c78c65c9b45p11bc0bjsnb62963bebfac",
            "X-RapidAPI-Host": "ind-nutrient-api1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        df = pd.json_normalize(
            data['cores'],
            'related_food',
            ['core_type', 'related_food_length'],
            errors='ignore'
        )
        protein=[]
        carbohydrates=[]
        fat=[]
        for ele in df['food_nutrition']:
            for nutri in ele:
                if nutri['nutrient_name']=='carbohydrates':
                    carbohydrates.append(nutri['value'])
                if nutri['nutrient_name']=='fat':
                    fat.append(nutri['value'])
                if nutri['nutrient_name']=='protein':
                    protein.append(nutri['value'])
                


        df['protein']=protein
        df['carbohydrates']=carbohydrates
        df['fat']=fat

        return df

    def food_recommendation(self, food_type, specifications, core=[]):
        print(food_type, specifications, core) 
        print(type(food_type),type(specifications),type(core))
        if food_type == "3":
            food = self.df
        elif food_type=="2":
            food = self.df[self.df['type'] == 'Non Vegetarian']
        else:
            food = self.df[self.df['type'] == 'Vegetarian']
        recommendations = []
       # print(food) 
        if core == ['Surprise']:
            random_food = food.sample(n=2)
            print(random_food)
            recommendations.append(random_food[['food_name', 'quantity', 'calories', 'protein', 'carbohydrates', 'fat']].reset_index(drop=True))
            return recommendations, True
            #return random_food[['food_name', 'quantity', 'calories', 'protein', 'carbohydrates', 'fat']].reset_index(drop=True), True
        else:
            core_list = []
            for item in core:
                core_food = food[food['core'] == item]
                core_list.append(core_food)

            
            for item in core_list:
                if specifications == '1':
                    avg = item['protein'].mean()
                    item = item[item['protein'] > avg]
                    random_food = item.sample(n=1 if len(item) >= 1 else len(item))
                    print(random_food)
                    recommendations.append(random_food[['food_name', 'quantity', 'calories', 'protein', 'carbohydrates', 'fat']].reset_index(drop=True))
                elif specifications == '2':
                    avg_carb = item['carbohydrates'].mean()
                    avg_fat = item['fat'].mean()
                    item = item[(item['carbohydrates'] < avg_carb) & (item['fat'] < avg_fat)]
                    random_food = item.sample(n=1 if len(item) >= 1 else len(item))
                    print(random_food)
                    recommendations.append(random_food[['food_name', 'quantity', 'calories', 'protein', 'carbohydrates', 'fat']].reset_index(drop=True))
                else:
                    random_food = item.sample(n=1 if len(item) >= 1 else len(item))
                    print(random_food)
                    recommendations.append(random_food[['food_name', 'quantity', 'calories', 'protein', 'carbohydrates', 'fat']].reset_index(drop=True))

            return recommendations, False

