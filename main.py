import pandas as pd
from datetime import datetime
from jinja2 import Template, FileSystemLoader, Environment

class CustomDate:
    POSSIBLE_DATE_FORMATS = ["%Y-%m-%d", "%Y-%m", "%Y"]

    def __init__(self, date_str, format):
        self.date = datetime.strptime(date_str, format)
        self.format = format

    def to_string(self, format=None):
        format = format if format else self.format
        return self.date.strftime(format)
    
    @classmethod
    def parse_datetime(cls, date_str):
        for fmt in cls.POSSIBLE_DATE_FORMATS:
            try:
                return cls(date_str, fmt)
            except ValueError:
                continue

        raise RuntimeError(f"Error: Unable to parse date {date_str}")

def main():
    df = pd.read_csv('input.csv', delimiter=';')

    def generate_family_tree(df):
        family_tree = {}
        for _, row in df.iterrows():
            birth_date = CustomDate.parse_datetime(row["birth_date"]) if pd.notna(row["birth_date"]) else None
            death_date = CustomDate.parse_datetime(row["death_date"]) if pd.notna(row["death_date"]) else None
            age = death_date.date.year - birth_date.date.year if birth_date and death_date else None  
            
            marriage_dates = eval(row["marriage_dates"]) if pd.notna(row["marriage_dates"]) else []
            marriage_dates = [CustomDate.parse_datetime(date) for date in marriage_dates]
            marriage_ages = [marriage_date.date.year - birth_date.date.year for marriage_date in marriage_dates]

            person = {
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "birth": birth_date.to_string() if birth_date else "???",
                "death": death_date.to_string() if death_date else "???",
                "age": age if age is not None else "???",
                "marriage_dates": [date.to_string() for date in marriage_dates],
                "marriage_ages": [age if age else "???" for age in marriage_ages],
                "spouses": eval(row["spouses"]) if pd.notna(row["spouses"]) else [],
                "parents": eval(row["parents"]) if pd.notna(row["parents"]) else [],
                "children": []
            }

            assert len(person["marriage_dates"]) == len(person["spouses"]), \
                f"Mismatch in number of marriage dates and number of spouses for person {person['first_name']} {person['last_name']}"

            family_tree[person["id"]] = person

        for person in family_tree.values():
            for parent_id in person["parents"]:
                family_tree[parent_id]["children"].append(person["id"])
                
        return family_tree

    family_tree = generate_family_tree(df)

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.html")
    html_content = template.render(family=family_tree)

    with open("family_tree.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Family tree HTML generated.")

if __name__ == "__main__":
    main()