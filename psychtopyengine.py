import os, pickle, json, sys


def main():
    data = None
    arrow_types = {}
    version = 1
    chart = input("(Add your chart.json (Psych only))>>")
    if not os.path.exists(chart):
        print("File doesn't exist, quitting..")
        sys.exit(1)
    with open(chart, "r") as f:
        data = json.load(f)
    print(f"Loaded chart: {data}")
    print(
        "Welcome to chart converter from Psych Engine to PyEngine.\nTo start with, you need to add all the players, from 1 to the maximum in the chart."
    )
    data = data["song"]
    data["speed"] = data["speed"] * 1.5
    sections = data["notes"]
    s = input("set arrow type > ")
    data.update({"arrow_type": s})
    data.update({"pyengine_version": version})
    for section in sections:
        notes = section["sectionNotes"]
        for note in notes:
            if str(note[1]) not in arrow_types:
                print(arrow_types)
                u = input(
                    f"What does the event number: {str(note[1])} do?\nSet the event here>>"
                )
                arrow_types.update({f"{note[1]}": u})

                note[1] = u
            else:
                note[1] = arrow_types[str(note[1])]
    newname = f"{chart.split('.')[0]}-converted.json"
    newdata = {"song": data}

    with open(newname, "w") as f:
        json.dump(newdata, f)
    print(f"Saved as {newname}")
    print("Successfully done everything, bye bye!!")
    input("[PRESS ENTER TO LEAVE]")


if __name__ == "__main__":
    main()
