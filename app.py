from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/monngon'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MonAn(db.Model):
    __tablename__ = 'mon_an'
    id = db.Column(db.Integer, primary_key=True)
    ten_mon = db.Column(db.String(255))
    hinh_anh = db.Column(db.String(255))
    link = db.Column(db.String(255))

class ChiTiet(db.Model):
    __tablename__ = 'chi_tiet_mon_an'
    id = db.Column(db.Integer, primary_key=True)
    mon_an_id = db.Column(db.Integer)
    nguyen_lieu = db.Column(db.Text)
    cach_nau = db.Column(db.Text)
    noi_dung_html = db.Column(db.Text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def list_monan():
    keyword = request.args.get('keyword', '')
    sort = request.args.get('sort', 'moi')
    page = int(request.args.get('page', 1))
    per_page = 5

    query = MonAn.query

    if keyword:
        query = query.filter(MonAn.ten_mon.like(f"%{keyword}%"))

    if sort == 'az':
        query = query.order_by(MonAn.ten_mon.asc())
    elif sort == 'za':
        query = query.order_by(MonAn.ten_mon.desc())
    else:
        query = query.order_by(MonAn.id.desc())

    total_results = query.count()
    mons = query.offset((page - 1) * per_page).limit(per_page).all()
    total_pages = (total_results + per_page - 1) // per_page

    return render_template("list.html",
                           mons=mons,
                           keyword=keyword,
                           sort=sort,
                           page=page,
                           total_pages=total_pages,
                           total_results=total_results)

@app.route('/chitiet/<int:id>')
def chitiet(id):
    mon = MonAn.query.get_or_404(id)
    chi_tiet = ChiTiet.query.filter_by(mon_an_id=id).first()
    return render_template('chitiet.html', mon=mon, chi_tiet=chi_tiet)

if __name__ == '__main__':
    app.run(debug=True)
