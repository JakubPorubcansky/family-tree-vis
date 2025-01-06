import pandas as pd
from jinja2 import Template, FileSystemLoader, Environment

def main():
    # Load the CSV file.
    df = pd.read_csv('input.csv', delimiter=';')

    # Start with the root of the family tree.
    def generate_family_tree(df):
        family_tree = {}
        for _, row in df.iterrows():
            person = {
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "birth": row["birth_date"] if pd.notna(row["birth_date"]) else "???",
                "death": row["death_date"] if pd.notna(row["death_date"]) else "???",
                "marriage_dates": eval(row["marriage_dates"]) if pd.notna(row["marriage_dates"]) else [],
                "spouses": eval(row["spouses"]) if pd.notna(row["spouses"]) else [],
                "parents": eval(row["parents"]) if pd.notna(row["parents"]) else [],
                "children": []
            }

            assert len(person["marriage_dates"]) == len(person["spouses"]), \
                "Mismatch in number of marriage dates and number of spouses for person {} {}".format(person["first_name"], person["last_name"])

            family_tree[person["id"]] = person

        for person in family_tree.values():
            for parent_id in person["parents"]:
                family_tree[parent_id]["children"].append(person["id"])
                
        return family_tree

    family_tree = generate_family_tree(df)

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')
    html_content = template.render(family=family_tree)

    # Write to an HTML file.
    with open('family_tree.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Family tree HTML generated.")

if __name__ == "__main__":
    main()