def add_book(data, ISBNCode, title ,author, year):
    pass

def delete_book(data, ISBNCode):
    pass

def borrow_book(ISBNCode):
    global data, headers, update
    update_status = False
    for book in data:
        if book['ISBN Code'].strip('*')==ISBNCode.strip():
            if book['Available'].strip().lower()=='yes':
                book['Popularity'] = int(book['Popularity']) + 1
                book['Available']='No'
                update_status = True
                update = f"Book '{book['Title']}' borrowed successfully."
                with open("data/library.csv",'w') as f:
                    writer = csv.DictWriter(f, headers)
                    writer.writeheader()
                    for row in data:
                        # Ensure only valid keys are written
                        filtered_row = {key: row.get(key, "") for key in headers}
                        writer.writerow(filtered_row)
            else:
                update = "Invalid operation."
                update_status = True
    if not update_status:
        update = "Book records not found"

def return_book(ISBNCode):
    global data, headers, update
    update_status = False
    for book in data:
        if book['ISBN Code'].strip('*')==ISBNCode.strip():
            if book['Available'].strip().lower()=='no':
                book['Available']='Yes'
                update_status = True
                update = f"Book '{book['Title']}' returned successfully."
                with open("data/library.csv",'w') as f:
                    writer = csv.DictWriter(f, headers)
                    writer.writeheader()
                    for row in data:
                        # Ensure only valid keys are written
                        filtered_row = {key: row.get(key, "") for key in headers}
                        writer.writerow(filtered_row)
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

if __name__=='__main__':
    app.run(debug=True)