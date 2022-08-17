import requests
import datetime

# Id dos restaurantes no backend
RESTAURANT_MAP ={
    "santa": 6, 
    "capao": 4,
    "ceu": 7,
    "anglo": 8
}

def get_query_string(date: str, restaurant: str) -> str:
  return f"https://cobalto.ufpel.edu.br/portal/cardapios/cardapioPublico/listaCardapios?null&txtData={date}&cmbRestaurante={restaurant}&_search=false&nd=1656779148361&rows=20&page=1&sidx=refeicao+asc%2C+id&sord=asc"

def get_restaurant_meals(res: dict) -> dict:
  meals = {}
  for row in res["rows"]:
   if row["refeicao"] not in meals:
      meals[row["refeicao"]] = []
  
   meals[row["refeicao"]].append(
       (row["nome"], row["descricao"])
    )
  return meals

def get_menus():
    menus = {}
    tdy = datetime.date.today()
    for restaurant in RESTAURANT_MAP:  
      res = requests.get(
          get_query_string(date=f"{tdy.day}/{tdy.month}/{tdy.year}",
          restaurant=RESTAURANT_MAP[restaurant])
      ).json()

      if "rows" not in res:
        menus[restaurant] = "Não haverão refeições nesse restaurante"
        continue
      menus[restaurant] = get_restaurant_meals(res=res)
    return menus

def format_meal(meal: list[tuple], title) -> str:  
  txt = f"{title}\n"
  for item, desc in meal:
    txt += f"   {item.lower()}\n"
  txt += "\n\n"
  
  return txt