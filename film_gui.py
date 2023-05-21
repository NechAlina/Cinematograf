import tkinter as tk
import pyodbc

# Specify the Access database file path
db_path = r"C:\Users\IT School\Documents\Final.accdb"

# Establish the database connection
conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + db_path)
cursor = conn.cursor()

def show_film_information():
    film_code = entry.get()

    # Execute the SQL query to retrieve film information
    query = """
    SELECT F.Nume, F.Regizor, F.Tip_film, F.Data_premiera, F.Audienta, B.Pret_bilet, B.Ora_desfasurare, B.NrBileteVandute
    FROM Filme AS F
    INNER JOIN Bilete AS B ON F.Cod_film = B.Cod_film
    WHERE F.Cod_film = ?
    """
    cursor.execute(query, film_code)

    # Fetch the retrieved data
    film_info = cursor.fetchone()

    if film_info:
        film_name = film_info[0]
        audience_rating = film_info[4]

        # Display the film information with warnings
        result_text = f"Informatii film:\n" \
                      f"Nume: {film_name}\n" \
                      f"Regizor: {film_info[1]}\n" \
                      f"Tip film: {film_info[2]}\n" \
                      f"Data premiera: {film_info[3]}\n" \
                      f"Audienta: {audience_rating}\n" \
                      f"Pret bilet: {film_info[5]}\n" \
                      f"Ora desfasurare: {film_info[6]}\n" \
                      f"Numar bilete vandute: {film_info[7]}\n"

        if audience_rating == "+15":
            result_text += "Numai cu acordul parintilor!"
        elif audience_rating == "+18":
            result_text += "Interzis minorilor!"

        result_label.config(text=result_text)
    else:
        # Display an error message if the film is not found
        result_label.config(text="Filmul nu exista/cod incorect!")



def show_top_films():
    # Execute the SQL query to retrieve top films based on ticket sales
    query = """
    SELECT F.Nume, F.Regizor, F.Tip_film, F.Data_premiera, B.Pret_bilet, B.Ora_desfasurare, B.NrBileteVandute, F.Audienta
    FROM Filme AS F
    INNER JOIN Bilete AS B ON F.Cod_film = B.Cod_film
    ORDER BY B.NrBileteVandute DESC
    """
    cursor.execute(query)

    # Fetch all the retrieved data
    films = cursor.fetchall()

    if films:
        # Display the film information
        result_text = "Top vanzari bilete:\n\n"
        for film in films:
            film_name = film[0]
            audience_rating = film[7]
            warnings = ""

            if audience_rating == "+18":
                warnings += "Interzis minorilor! "
            elif audience_rating == "+15":
                warnings += "Numai cu acordul parintilor! "

            result_text += f"Nume: {film_name}\n"
            result_text += f"Regizor: {film[1]}\n"
            result_text += f"Tip film: {film[2]}\n"
            result_text += f"Pret bilet: {film[4]}\n"
            result_text += f"Numar bilete vandute: {film[6]}\n"
            result_text += f"Audienta: {audience_rating}\n"
            result_text += warnings
            result_text += "\n"

        result_label.config(text=result_text)
    else:
        # Display an error message if no films are found
        result_label.config(text="Nu exista filme inregistrate.")


# Create the GUI window
window = tk.Tk()
window.title("Informatii film")

# Create GUI elements
label = tk.Label(window, text="Introdu codul filmului:")
label.pack()

entry = tk.Entry(window)
entry.pack()

info_button = tk.Button(window, text="Afiseaza informatii film", command=show_film_information)
info_button.pack()

top_films_button = tk.Button(window, text="Top Vanzari Bilete", command=show_top_films)
top_films_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

# Run the GUI event loop
window.mainloop()

# Close the cursor and the database connection
cursor.close()
conn.close()
