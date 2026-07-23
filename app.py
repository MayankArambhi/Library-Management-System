def write_data():
    global data, headers
    with open("data/library.csv",'w') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for row in data:
            # Ensure only valid keys are written
            filtered_row = {key: row.get(key, "") for key in headers}
            writer.writerow(filtered_row)

def add_book(ISBNCode, title ,author, year):
    global data, update
    if ISBNCode not in [book['ISBN Code'].strip() for book in data]:
        data.append(
            {'Title': title, 'Author': author, 'Year': year, 'Available': 'Yes','ISBN Code': ISBNCode, 'Popularity': 0}
        )
        write_data()
        update = f"Book \"{title}\" listed successfully"
    else: 
        update = 'Book already exists. Check ISBN Code'

def delete_book(ISBNCode):
    global data, update
    for book in data:
        if book['ISBN Code'].strip('*') == ISBNCode:
            data.remove(book)
            write_data()
            update = f"Book \"{book['Title']}\" delisted from the library."
            return
    update = f"Could not find the ISBN {ISBNCode}."

def borrow_book(ISBNCode):
    global data, update
    update_status = False
    for book in data:
        if book['ISBN Code'].strip('*')==ISBNCode.strip():
            if book['Available'].strip().lower()=='yes':
                book['Popularity'] = int(book['Popularity']) + 1
                book['Available']='No'
                update_status = True
                update = f"Book \"{book['Title']}\" borrowed successfully."
                write_data()
            else:
                update = "Invalid operation."
                update_status = True
    if not update_status:
        update = "Book records not found"

def return_book(ISBNCode):
    global data, update
    update_status = False
    for book in data:
        if book['ISBN Code'].strip('*')==ISBNCode.strip():
            if book['Available'].strip().lower()=='no':
                book['Available']='Yes'
                update_status = True
                update = f"Book \"{book['Title']}\" returned successfully."
                write_data()
            else:
                update = "Invalid operation."
                update_status = True
    if not update_status:
        update = "Book records not found"

update = ""

import csv
with open("data/library.csv",'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)
    headers = data[0].keys()

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    global update
    if request.method=='POST':
        ISBN = request.form.get('isbn')
        if request.form.get('rb')=='borrow':
            borrow_book(ISBN)
        elif request.form.get('rb')=='return':
            return_book(ISBN)
        else:
            update = ""
        return render_template('index.html',data=data, update=update)
    return render_template('index.html',data=data)

@app.route("/manage", methods=["GET","POST"])
def manage():
    global update
    if request.method=='POST':
        form_type = request.form.get("form-type")
        isbn = request.form.get("isbn")
        if form_type=="List":
            title = request.form.get("title")
            author = request.form.get("author")
            year = request.form.get("year")
            add_book(isbn, title, author, year)
        elif form_type == "De-list":
            delete_book(isbn)
        else: update=""
        return render_template('manage.html',data=data, update=update)
    return render_template("manage.html", data=data)

if __name__=='__main__':
    app.run(debug=True)