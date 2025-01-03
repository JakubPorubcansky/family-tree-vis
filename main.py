import pandas as pd
from jinja2 import Template, FileSystemLoader, Environment

def main():
    # Load the CSV file.
    df = pd.read_csv('input.csv', delimiter=',')

    # Start with the root of the family tree.
    def generate_family_tree(df):
        family_tree = {}
        for _, row in df.iterrows():
            person = {
                "id": row["id"],
                "first_name": row["meno"],
                "last_name": row["priezvisko"],
                "birth": row["datum_narodenia"],
                "death": row["datum_umrtia"],
                "spouses": eval(row["sobaseny_s"]) if pd.notna(row["sobaseny_s"]) else [],
                "parents": eval(row["rodicia"]) if pd.notna(row["rodicia"]) else [],
                "children": []
            }
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