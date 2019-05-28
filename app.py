import os

from flask import Flask, render_template
from piecash import open_book

app = Flask(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def hello_world():
    s = open_book(os.path.join(base_dir, 'CommonDB.gnucash'))
    print(s.default_currency)
    rows = []
    for tr in sorted(s.transactions, key=lambda x: x.post_date):
        rows.append({
            'name': "- {:%Y/%m/%d} : {}".format(tr.post_date, tr.description),
            'splits': [
                "\t{amount}  {direction}  {account} : {memo}".format(
                    amount=abs(spl.value),
                    direction="-->" if spl.value > 0 else "paid by",
                    account=spl.account.fullname,
                    memo=spl.memo
                ) for spl in tr.splits
            ]
        })
    return render_template('index.html', **{'rows': rows})


if __name__ == '__main__':
    app.run()
