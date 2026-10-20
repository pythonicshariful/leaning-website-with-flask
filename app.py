import os
import uuid
from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

import db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "svg", "gif"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def taka(n):
    try:
        n = int(n)
        return f"৳{n:,}".replace(",", ",")
    except Exception:
        return f"৳{n}"


app.jinja_env.filters["taka"] = taka


# ============================================================================
# CONTEXT PROCESSOR (Injects settings, nav, year into every single template)
# ============================================================================
@app.context_processor
def inject_global_data():
    settings = db.get_settings()
    nav = db.get_nav()
    offers = [o for o in db.get_offers() if o.get("is_active")]
    active_offer = offers[0] if offers else None
    return {
        "year": datetime.now().year,
        "settings": settings,
        "nav_items": nav,
        "active_offer": active_offer,
    }


# ============================================================================
# AUTHENTICATION DECORATOR FOR ADMIN
# ============================================================================
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("অ্যাডমিন প্যানেল ব্যবহার করতে অনুগ্রহ করে লগইন করুন।")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)

    return decorated_function


# ============================================================================
# PUBLIC FRONTEND ROUTES (CONNECTED DIRECTLY TO DB)
# ============================================================================
@app.route("/")
def index():
    courses = db.get_courses()
    workshops = db.get_workshops()
    posts = db.get_posts()[:3]
    trust = db.get_trust()
    features = db.get_features()
    return render_template(
        "index.html",
        featured=courses,
        workshops=workshops,
        posts=posts,
        trust_items=trust,
        feature_items=features,
    )


@app.route("/courses")
def courses():
    cat = request.args.get("cat", "")
    all_courses = db.get_courses()
    items = all_courses
    if cat:
        items = [c for c in all_courses if c.get("category") == cat]
    cats = sorted({c.get("category") for c in all_courses if c.get("category")})
    return render_template("courses.html", courses=items, cats=cats, cat=cat)


@app.route("/course/<cid>")
def course(cid):
    item = db.get_course(cid)
    if not item:
        return render_template("notfound.html"), 404
    all_courses = db.get_courses()
    others = [c for c in all_courses if c.get("id") != cid][:3]
    return render_template("course.html", c=item, others=others)


@app.route("/bundles")
def bundles():
    raw_bundles = db.get_bundles()
    packed = []
    for b in raw_bundles:
        inc_ids = b.get("includes", [])
        c_list = [db.get_course(i) for i in inc_ids if db.get_course(i)]
        packed.append({**b, "courses": c_list})
    return render_template("bundles.html", bundles=packed)


@app.route("/workshops")
def workshops():
    items = db.get_workshops()
    return render_template("workshops.html", workshops=items)


@app.route("/ebooks")
def ebooks():
    items = db.get_ebooks()
    return render_template("ebooks.html", ebooks=items)


@app.route("/blog")
def blog():
    q = request.args.get("q", "").strip().lower()
    items = db.get_posts()
    if q:
        items = [
            p
            for p in items
            if q in p.get("title", "").lower()
            or q in p.get("body", "").lower()
            or q in p.get("tag", "").lower()
        ]
    return render_template("blog.html", posts=items, q=q)


@app.route("/about")
def about():
    team = db.get_team()
    # Team can be list of dicts: [{"name": "...", "role": "..."}]
    team_tuples = [(m.get("name"), m.get("role")) for m in team]
    return render_template("about.html", team=team_tuples)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        message = request.form.get("msg", "").strip()
        if name and phone:
            db.add_message({
                "type": "contact",
                "name": name,
                "phone": phone,
                "message": message,
            })
            flash("ধন্যবাদ! আপনার মেসেজ রেকর্ড হয়েছে। শীঘ্রই যোগাযোগ করা হবে।")
        else:
            flash("অনুগ্রহ করে আপনার নাম ও ফোন নম্বর লিখুন।")
        return redirect(url_for("contact"))
    return render_template("contact.html")


def get_current_student():
    student_id = session.get("student_id")
    if not student_id:
        return None
    return db.get_student(student_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone", "").strip()
        name = request.form.get("name", "").strip() or "শিক্ষার্থী"
        if not phone:
            flash("অনুগ্রহ করে মোবাইল নম্বর লিখুন।")
            return redirect(url_for("login"))

        student = db.find_student_by_phone(phone)
        if not student:
            student = db.save_student({
                "name": name,
                "phone": phone,
                "email": "",
                "photo": "",
            })
        session["student_id"] = student["id"]
        session["student_name"] = student.get("name", name)
        flash(f"স্বাগতম, {student.get('name', 'শিক্ষার্থী')}! আপনার ড্যাশবোর্ডে প্রবেশ করেছেন।")
        return redirect(url_for("student_dashboard"))
    return render_template("login.html")


@app.route("/student")
def student_index():
    return redirect(url_for("student_dashboard"))


@app.route("/student/logout")
def student_logout():
    session.pop("student_id", None)
    session.pop("student_name", None)
    flash("সফলভাবে লগআউট করেছেন।")
    return redirect(url_for("login"))


@app.route("/student/dashboard")
def student_dashboard():
    student = get_current_student()
    if not student:
        flash("আপনার ড্যাশবোর্ড দেখতে লগইন করুন।")
        return redirect(url_for("login"))

    paid_orders = []
    for order in db.get_orders_for_student(student["id"]):
        course = None
        if order.get("kind") == "course":
            course = db.get_course(order.get("item_id"))
        elif order.get("kind") == "workshop":
            for item in db.get_workshops():
                if item.get("id") == order.get("item_id"):
                    course = item
                    break
        elif order.get("kind") == "bundle":
            for item in db.get_bundles():
                if item.get("id") == order.get("item_id"):
                    course = item
                    break
        if not course:
            continue

        progress = db.get_student_course_progress(student["id"], order.get("item_id"))
        paid_orders.append({
            "order": order,
            "course": course,
            "progress": progress,
        })

    payments = db.get_payments_for_student(student["id"])
    return render_template(
        "student_dashboard.html",
        student=student,
        purchased=paid_orders,
        total_courses=len(paid_orders),
        payments=payments,
    )


@app.route("/student/profile", methods=["GET", "POST"])
def student_profile():
    student = get_current_student()
    if not student:
        flash("আপনার প্রোফাইল দেখতে লগইন করুন।")
        return redirect(url_for("login"))

    if request.method == "POST":
        student["name"] = request.form.get("name", student.get("name", "")).strip() or student.get("name", "শিক্ষার্থী")
        student["email"] = request.form.get("email", "").strip()
        student["phone"] = request.form.get("phone", student.get("phone", "")).strip()
        student["photo"] = request.form.get("photo", student.get("photo", "")).strip()
        db.save_student(student)
        flash("প্রোফাইল আপডেট করা হয়েছে।")
        return redirect(url_for("student_profile"))

    return render_template("student_profile.html", student=student)


@app.route("/student/progress/<cid>", methods=["POST"])
def student_progress(cid):
    student = get_current_student()
    if not student:
        return jsonify({"ok": False, "message": "login required"}), 401

    payload = request.get_json(silent=True) or request.form
    percent = int(payload.get("percent", 0) or 0)
    watched_seconds = int(payload.get("watched_seconds", 0) or 0)
    if not isinstance(percent, int):
        try:
            percent = int(float(percent))
        except Exception:
            percent = 0

    record = db.save_course_progress(student["id"], cid, {
        "percent": percent,
        "watched_seconds": watched_seconds,
    })
    return jsonify({"ok": True, "percent": record["percent"], "status": record["status"], "watched_seconds": record["watched_seconds"]})


@app.route("/verify", methods=["GET", "POST"])
def verify():
    result = None
    code = ""
    certs = db.get_certs()
    if request.method == "POST":
        code = request.form.get("code", "").strip().upper()
        result = certs.get(code, False)
    return render_template("verify.html", result=result, code=code)


@app.route("/legal/<page>")
def legal(page):
    legals = db.get_legal()
    if page not in legals:
        return render_template("notfound.html"), 404
    data = legals[page]
    return render_template(
        "legal.html", title=data.get("title"), page=page, content=data.get("content")
    )


@app.route("/enroll/<kind>/<cid>", methods=["POST"])
def enroll(kind, cid):
    student = get_current_student()
    if not student:
        flash("কোর্স কিনতে অথবা অ্যাক্সেস নিতে আগে লগইন করুন।")
        return redirect(url_for("login"))

    item_title = cid
    amount = 0
    if kind == "course":
        c = db.get_course(cid)
        if c:
            item_title = c.get("title")
            amount = int(c.get("price") or 0)
    elif kind == "workshop":
        for w in db.get_workshops():
            if w.get("id") == cid:
                item_title = w.get("title")
                amount = int(w.get("price") or 0)
                break
    elif kind == "bundle":
        for b in db.get_bundles():
            if b.get("id") == cid:
                item_title = b.get("title")
                amount = int(b.get("price") or 0)
                break
    elif kind == "ebook":
        for e in db.get_ebooks():
            if e.get("id") == cid:
                item_title = e.get("title")
                amount = int(e.get("price") or 0)
                break

    order = db.add_order({
        "student_id": student["id"],
        "kind": kind,
        "item_id": cid,
        "item_title": item_title,
        "amount": amount,
        "status": "paid",
        "payment_method": "manual",
        "ip": request.remote_addr,
    })
    db.add_payment({
        "student_id": student["id"],
        "order_id": order["id"],
        "amount": amount,
        "status": "paid",
        "payment_method": "manual",
        "reference": f"ord-{order['id']}",
    })
    db.add_enrollment({
        "kind": kind,
        "item_id": cid,
        "item_title": item_title,
        "student_id": student["id"],
        "status": "paid",
        "amount": amount,
        "ip": request.remote_addr,
    })
    flash(f"অভিনন্দন! '{item_title}' আপনার কোর্স তালিকায় যুক্ত হয়েছে।")
    return redirect(url_for("student_dashboard"))


# ============================================================================
# ADMIN AUTHENTICATION
# ============================================================================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        admin_username = os.environ.get("ADMIN_USERNAME")
        admin_password = os.environ.get("ADMIN_PASSWORD")
        if not admin_username or not admin_password:
            flash("Admin login is not configured. Set ADMIN_USERNAME and ADMIN_PASSWORD.")
        elif username == admin_username and password == admin_password:
            session["admin_logged_in"] = True
            session["admin_username"] = username
            flash("সফলভাবে অ্যাডমিন ড্যাশবোর্ডে লগইন করেছেন!")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("ভুল ইউজারনেম অথবা পাসওয়ার্ড! পুনরায় চেষ্টা করুন।")

    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)
    flash("সফলভাবে লগআউট হয়েছে।")
    return redirect(url_for("admin_login"))


# ============================================================================
# ADMIN DASHBOARD & OVERVIEW
# ============================================================================
@app.route("/admin")
@admin_required
def admin_dashboard():
    courses = db.get_courses()
    workshops = db.get_workshops()
    bundles = db.get_bundles()
    ebooks = db.get_ebooks()
    posts = db.get_posts()
    messages = db.get_messages()
    enrollments = db.get_enrollments()
    return render_template(
        "admin/dashboard.html",
        active_page="dashboard",
        courses=courses,
        workshops=workshops,
        bundles=bundles,
        ebooks=ebooks,
        posts=posts,
        messages=messages,
        enrollments=enrollments,
    )


# ============================================================================
# ADMIN: SITE SETTINGS (GLOBAL, HEADER, OFFER BAR, FOOTER, CONTACT, SEO)
# ============================================================================
@app.route("/admin/settings", methods=["GET", "POST"])
@admin_required
def admin_settings():
    settings = db.get_settings()
    if request.method == "POST":
        form_data = request.form.to_dict()
        # Handle checkboxes (if active)
        form_data["announcement_active"] = "announcement_active" in request.form
        db.update_settings(form_data)
        flash("সাইট সেটিংস ও ব্যানার সফলভাবে আপডেট করা হয়েছে!")
        return redirect(url_for("admin_settings"))

    return render_template("admin/settings.html", active_page="settings", settings=settings)


# ============================================================================
# ADMIN: NAVIGATION MENU (Header Links)
# ============================================================================
@app.route("/admin/menu", methods=["GET", "POST"])
@admin_required
def admin_menu():
    if request.method == "POST":
        labels = request.form.getlist("label")
        urls = request.form.getlist("url")
        endpoints = request.form.getlist("endpoint")
        new_nav = []
        for i in range(len(labels)):
            if labels[i].strip():
                new_nav.append({
                    "label": labels[i].strip(),
                    "url": urls[i].strip() if i < len(urls) else "/",
                    "endpoint": endpoints[i].strip() if i < len(endpoints) else "",
                })
        db.save_nav(new_nav)
        flash("হেডার মেনু তালিকা সফলভাবে আপডেট করা হয়েছে!")
        return redirect(url_for("admin_menu"))

    nav = db.get_nav()
    return render_template("admin/menu.html", active_page="menu", nav=nav)


# ============================================================================
# ADMIN: HOMEPAGE SECTIONS (Hero, Trust Strip, Features)
# ============================================================================
@app.route("/admin/homepage", methods=["GET", "POST"])
@admin_required
def admin_homepage():
    settings = db.get_settings()
    trust = db.get_trust()
    features = db.get_features()

    if request.method == "POST":
        # Handle file upload for hero image if present
        hero_file = request.files.get("hero_image_file")
        hero_image_path = request.form.get("hero_image")
        if hero_file and hero_file.filename and allowed_file(hero_file.filename):
            fname = f"hero_{uuid.uuid4().hex[:8]}_{secure_filename(hero_file.filename)}"
            hero_file.save(os.path.join(app.config["UPLOAD_FOLDER"], fname))
            hero_image_path = f"/static/uploads/{fname}"

        # Update hero & headings in settings
        settings_update = {
            "hero_pill": request.form.get("hero_pill", ""),
            "hero_title": request.form.get("hero_title", ""),
            "hero_desc": request.form.get("hero_desc", ""),
            "hero_btn1_text": request.form.get("hero_btn1_text", ""),
            "hero_btn1_link": request.form.get("hero_btn1_link", ""),
            "hero_btn2_text": request.form.get("hero_btn2_text", ""),
            "hero_btn2_link": request.form.get("hero_btn2_link", ""),
            "hero_image": hero_image_path,
            "hero_stat_students": request.form.get("hero_stat_students", ""),
            "hero_stat_students_label": request.form.get("hero_stat_students_label", ""),
            "hero_stat_rating": request.form.get("hero_stat_rating", ""),
            "hero_stat_rating_label": request.form.get("hero_stat_rating_label", ""),
            "hero_stat_projects": request.form.get("hero_stat_projects", ""),
            "hero_stat_projects_label": request.form.get("hero_stat_projects_label", ""),
            "hero_float1_title": request.form.get("hero_float1_title", ""),
            "hero_float1_desc": request.form.get("hero_float1_desc", ""),
            "hero_float2_title": request.form.get("hero_float2_title", ""),
            "hero_float2_desc": request.form.get("hero_float2_desc", ""),
            "courses_tag": request.form.get("courses_tag", ""),
            "courses_title": request.form.get("courses_title", ""),
            "courses_desc": request.form.get("courses_desc", ""),
            "workshops_tag": request.form.get("workshops_tag", ""),
            "workshops_title": request.form.get("workshops_title", ""),
            "workshops_desc": request.form.get("workshops_desc", ""),
            "features_tag": request.form.get("features_tag", ""),
            "features_title": request.form.get("features_title", ""),
            "features_desc": request.form.get("features_desc", ""),
            "blog_tag": request.form.get("blog_tag", ""),
            "blog_title": request.form.get("blog_title", ""),
            "blog_desc": request.form.get("blog_desc", ""),
        }
        db.update_settings(settings_update)

        # Update Trust Strip items
        t_titles = request.form.getlist("trust_title")
        t_descs = request.form.getlist("trust_desc")
        t_icons = request.form.getlist("trust_icon")
        new_trust = []
        for i in range(len(t_titles)):
            if t_titles[i].strip():
                new_trust.append({
                    "title": t_titles[i].strip(),
                    "desc": t_descs[i].strip() if i < len(t_descs) else "",
                    "icon": t_icons[i].strip() if i < len(t_icons) else "check",
                })
        if new_trust:
            db.save_trust(new_trust)

        # Update Features
        f_titles = request.form.getlist("feature_title")
        f_descs = request.form.getlist("feature_desc")
        new_feat = []
        for i in range(len(f_titles)):
            if f_titles[i].strip():
                new_feat.append({
                    "title": f_titles[i].strip(),
                    "desc": f_descs[i].strip() if i < len(f_descs) else "",
                })
        if new_feat:
            db.save_features(new_feat)

        flash("হোমপেজের সকল সেকশন সফলভাবে সংরক্ষণ করা হয়েছে!")
        return redirect(url_for("admin_homepage"))

    return render_template(
        "admin/homepage.html",
        active_page="homepage",
        settings=settings,
        trust=trust,
        features=features,
    )


# ============================================================================
# ADMIN: OFFERS & DISCOUNTS
# ============================================================================
@app.route("/admin/offers")
@admin_required
def admin_offers():
    offers = db.get_offers()
    return render_template("admin/offers.html", active_page="offers", offers=offers)


@app.route("/admin/offers/save", methods=["POST"])
@admin_required
def admin_offer_save():
    oid = request.form.get("id", "").strip() or f"off-{uuid.uuid4().hex[:6]}"
    code = request.form.get("code", "").strip().upper()
    title = request.form.get("title", "").strip()
    val = request.form.get("discount_value", 0)
    try:
        val = int(val)
    except Exception:
        val = 0

    offer_data = {
        "id": oid,
        "code": code,
        "title": title,
        "discount_type": request.form.get("discount_type", "percent"),
        "discount_value": val,
        "valid_until": request.form.get("valid_until", "").strip(),
        "is_active": "is_active" in request.form,
        "note": request.form.get("note", "").strip(),
    }
    db.save_offer(offer_data)
    flash("অফার সফলভাবে সংরক্ষিত হয়েছে!")
    return redirect(url_for("admin_offers"))


@app.route("/admin/offers/delete/<oid>")
@admin_required
def admin_offer_delete(oid):
    db.delete_offer(oid)
    flash("অফারটি মুছে ফেলা হয়েছে।")
    return redirect(url_for("admin_offers"))


# ============================================================================
# ADMIN: COURSES CRUD
# ============================================================================
@app.route("/admin/courses")
@admin_required
def admin_courses():
    courses = db.get_courses()
    return render_template("admin/courses.html", active_page="courses", courses=courses)


@app.route("/admin/course/new", methods=["GET", "POST"])
@admin_required
def admin_course_new():
    if request.method == "POST":
        cid = request.form.get("id", "").strip()
        if not cid:
            flash("কোর্স আইডি দেওয়া আবশ্যক!")
            return redirect(url_for("admin_course_new"))

        # Image upload check
        img_file = request.files.get("image_file")
        img_path = request.form.get("image", "").strip() or "/static/images/courses/excel-office.jpg"
        if img_file and img_file.filename and allowed_file(img_file.filename):
            fname = f"course_{cid}_{uuid.uuid4().hex[:6]}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["UPLOAD_FOLDER"], fname))
            img_path = f"/static/uploads/{fname}"

        modules_raw = request.form.get("modules_text", "").splitlines()
        modules = [m.strip() for m in modules_raw if m.strip()]

        course_data = {
            "id": cid,
            "title": request.form.get("title", "").strip(),
            "short": request.form.get("short", "").strip(),
            "category": request.form.get("category", "অফিস").strip(),
            "level": request.form.get("level", "শুরুর দিক").strip(),
            "hours": int(request.form.get("hours", 15) or 15),
            "lessons": int(request.form.get("lessons", 30) or 30),
            "price": int(request.form.get("price", 1490) or 1490),
            "old": int(request.form.get("old", 2490) or 2490),
            "students": int(request.form.get("students", 1000) or 1000),
            "instructor": request.form.get("instructor", "").strip(),
            "role": request.form.get("role", "").strip(),
            "rating": float(request.form.get("rating", 4.9) or 4.9),
            "reviews": int(request.form.get("reviews", 100) or 100),
            "badge": request.form.get("badge", "চাকরির জন্য").strip(),
            "tag": request.form.get("tag", "বেস্টসেলার").strip(),
            "image": img_path,
            "modules": modules,
        }
        db.save_course(course_data, is_new=True)
        flash(f"'{course_data['title']}' কোর্সটি সফলভাবে তৈরি হয়েছে!")
        return redirect(url_for("admin_courses"))

    return render_template("admin/course_edit.html", active_page="courses", c=None)


@app.route("/admin/course/edit/<cid>", methods=["GET", "POST"])
@admin_required
def admin_course_edit(cid):
    c = db.get_course(cid)
    if not c:
        flash("কোর্সটি পাওয়া যায়নি!")
        return redirect(url_for("admin_courses"))

    if request.method == "POST":
        img_file = request.files.get("image_file")
        img_path = request.form.get("image", "").strip() or c.get("image")
        if img_file and img_file.filename and allowed_file(img_file.filename):
            fname = f"course_{cid}_{uuid.uuid4().hex[:6]}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["UPLOAD_FOLDER"], fname))
            img_path = f"/static/uploads/{fname}"

        modules_raw = request.form.get("modules_text", "").splitlines()
        modules = [m.strip() for m in modules_raw if m.strip()]

        course_data = {
            "id": cid,
            "title": request.form.get("title", "").strip(),
            "short": request.form.get("short", "").strip(),
            "category": request.form.get("category", "অফিস").strip(),
            "level": request.form.get("level", "শুরুর দিক").strip(),
            "hours": int(request.form.get("hours", 15) or 15),
            "lessons": int(request.form.get("lessons", 30) or 30),
            "price": int(request.form.get("price", 1490) or 1490),
            "old": int(request.form.get("old", 2490) or 2490),
            "students": int(request.form.get("students", 1000) or 1000),
            "instructor": request.form.get("instructor", "").strip(),
            "role": request.form.get("role", "").strip(),
            "rating": float(request.form.get("rating", 4.9) or 4.9),
            "reviews": int(request.form.get("reviews", 100) or 100),
            "badge": request.form.get("badge", "").strip(),
            "tag": request.form.get("tag", "").strip(),
            "image": img_path,
            "modules": modules,
        }
        db.save_course(course_data, is_new=False)
        flash(f"'{course_data['title']}' কোর্সটি আপডেট করা হয়েছে!")
        return redirect(url_for("admin_courses"))

    return render_template("admin/course_edit.html", active_page="courses", c=c)


@app.route("/admin/course/delete/<cid>")
@admin_required
def admin_course_delete(cid):
    db.delete_course(cid)
    flash("কোর্সটি সফলভাবে মুছে ফেলা হয়েছে।")
    return redirect(url_for("admin_courses"))


# ============================================================================
# ADMIN: WORKSHOPS CRUD
# ============================================================================
@app.route("/admin/workshops")
@admin_required
def admin_workshops():
    workshops = db.get_workshops()
    return render_template("admin/workshops.html", active_page="workshops", workshops=workshops)


@app.route("/admin/workshop/save", methods=["POST"])
@admin_required
def admin_workshop_save():
    wid = request.form.get("id", "").strip() or f"wk-{uuid.uuid4().hex[:6]}"
    title = request.form.get("title", "").strip()
    try:
        price = int(request.form.get("price", 0))
    except Exception:
        price = 0

    w_data = {
        "id": wid,
        "title": title,
        "when": request.form.get("when", "").strip(),
        "place": request.form.get("place", "").strip(),
        "seats": request.form.get("seats", "").strip(),
        "price": price,
    }
    db.save_workshop(w_data)
    flash(f"'{title}' ওয়ার্কশপটি সংরক্ষণ করা হয়েছে!")
    return redirect(url_for("admin_workshops"))


@app.route("/admin/workshop/delete/<wid>")
@admin_required
def admin_workshop_delete(wid):
    db.delete_workshop(wid)
    flash("ওয়ার্কশপটি মুছে ফেলা হয়েছে।")
    return redirect(url_for("admin_workshops"))


# ============================================================================
# ADMIN: BUNDLES CRUD
# ============================================================================
@app.route("/admin/bundles")
@admin_required
def admin_bundles():
    bundles = db.get_bundles()
    all_courses = db.get_courses()
    return render_template(
        "admin/bundles.html",
        active_page="bundles",
        bundles=bundles,
        all_courses=all_courses,
    )


@app.route("/admin/bundle/save", methods=["POST"])
@admin_required
def admin_bundle_save():
    bid = request.form.get("id", "").strip() or f"bundle-{uuid.uuid4().hex[:6]}"
    title = request.form.get("title", "").strip()
    includes = request.form.getlist("includes")
    try:
        price = int(request.form.get("price", 0))
        old = int(request.form.get("old", 0))
    except Exception:
        price, old = 0, 0

    b_data = {
        "id": bid,
        "title": title,
        "price": price,
        "old": old,
        "includes": includes,
        "note": request.form.get("note", "").strip(),
    }
    db.save_bundle(b_data)
    flash(f"'{title}' বান্ডেলটি সংরক্ষিত হয়েছে!")
    return redirect(url_for("admin_bundles"))


@app.route("/admin/bundle/delete/<bid>")
@admin_required
def admin_bundle_delete(bid):
    db.delete_bundle(bid)
    flash("বান্ডেলটি মুছে ফেলা হয়েছে।")
    return redirect(url_for("admin_bundles"))


# ============================================================================
# ADMIN: EBOOKS CRUD
# ============================================================================
@app.route("/admin/ebooks")
@admin_required
def admin_ebooks():
    ebooks = db.get_ebooks()
    return render_template("admin/ebooks.html", active_page="ebooks", ebooks=ebooks)


@app.route("/admin/ebook/save", methods=["POST"])
@admin_required
def admin_ebook_save():
    ebid = request.form.get("id", "").strip() or f"eb-{uuid.uuid4().hex[:6]}"
    title = request.form.get("title", "").strip()
    try:
        pages = int(request.form.get("pages", 10))
        price = int(request.form.get("price", 100))
    except Exception:
        pages, price = 10, 100

    eb_data = {
        "id": ebid,
        "title": title,
        "pages": pages,
        "price": price,
    }
    db.save_ebook(eb_data)
    flash(f"'{title}' ই-বুকটি সংরক্ষণ করা হয়েছে!")
    return redirect(url_for("admin_ebooks"))


@app.route("/admin/ebook/delete/<ebid>")
@admin_required
def admin_ebook_delete(ebid):
    db.delete_ebook(ebid)
    flash("ই-বুকটি মুছে ফেলা হয়েছে।")
    return redirect(url_for("admin_ebooks"))


# ============================================================================
# ADMIN: BLOG POSTS CRUD
# ============================================================================
@app.route("/admin/posts")
@admin_required
def admin_posts():
    posts = db.get_posts()
    return render_template("admin/posts.html", active_page="posts", posts=posts)


@app.route("/admin/post/save", methods=["POST"])
@admin_required
def admin_post_save():
    pid = request.form.get("id", "").strip() or f"post-{uuid.uuid4().hex[:6]}"
    title = request.form.get("title", "").strip()
    date_str = request.form.get("date", "").strip() or datetime.now().strftime("%d %b %Y")
    p_data = {
        "id": pid,
        "title": title,
        "date": date_str,
        "tag": request.form.get("tag", "ক্যারিয়ার").strip(),
        "body": request.form.get("body", "").strip(),
    }
    db.save_post(p_data)
    flash(f"'{title}' ব্লগ পোস্টটি সংরক্ষণ করা হয়েছে!")
    return redirect(url_for("admin_posts"))


@app.route("/admin/post/delete/<pid>")
@admin_required
def admin_post_delete(pid):
    db.delete_post(pid)
    flash("ব্লগ পোস্টটি মুছে ফেলা হয়েছে।")
    return redirect(url_for("admin_posts"))


# ============================================================================
# ADMIN: CERTIFICATES MANAGEMENT
# ============================================================================
@app.route("/admin/certs")
@admin_required
def admin_certs():
    certs = db.get_certs()
    return render_template("admin/certs.html", active_page="certs", certs=certs)


@app.route("/admin/cert/save", methods=["POST"])
@admin_required
def admin_cert_save():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip()
    course_name = request.form.get("course", "").strip()
    date_str = request.form.get("date", "").strip()
    if not code or not name:
        flash("সার্টিফিকেট কোড ও শিক্ষার্থীর নাম দেওয়া আবশ্যক!")
        return redirect(url_for("admin_certs"))

    db.save_cert(code, {"name": name, "course": course_name, "date": date_str})
    flash(f"সার্টিফিকেট কোড '{code}' সংরক্ষিত হয়েছে!")
    return redirect(url_for("admin_certs"))


@app.route("/admin/cert/delete/<code>")
@admin_required
def admin_cert_delete(code):
    db.delete_cert(code)
    flash(f"সার্টিফিকেট '{code}' মুছে ফেলা হয়েছে।")
    return redirect(url_for("admin_certs"))


# ============================================================================
# ADMIN: MESSAGES & ENROLLMENTS
# ============================================================================
@app.route("/admin/messages")
@admin_required
def admin_messages():
    messages = db.get_messages()
    enrollments = db.get_enrollments()
    return render_template(
        "admin/messages.html",
        active_page="messages",
        messages=messages,
        enrollments=enrollments,
    )


@app.route("/admin/message/delete/<mid>")
@admin_required
def admin_message_delete(mid):
    db.delete_message(mid)
    flash("মেসেজটি মুছে ফেলা হয়েছে।")
    return redirect(url_for("admin_messages"))


@app.route("/admin/enrollment/delete/<eid>")
@admin_required
def admin_enrollment_delete(eid):
    db.delete_enrollment(eid)
    flash("এনরোলমেন্টটি মুছে ফেলা হয়েছে।")
    return redirect(url_for("admin_messages"))


# ============================================================================
# ADMIN: LEGAL PAGES EDITING
# ============================================================================
@app.route("/admin/legal", methods=["GET", "POST"])
@admin_required
def admin_legal():
    legals = db.get_legal()
    if request.method == "POST":
        page_key = request.form.get("page_key")
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if page_key in legals:
            legals[page_key] = {"title": title, "content": content}
            db.save_legal(legals)
            flash(f"'{title}' পেজটি আপডেট করা হয়েছে!")
        return redirect(url_for("admin_legal"))

    return render_template("admin/legal.html", active_page="legal", legals=legals)


# ============================================================================
# ADMIN: TEAM MEMBERS
# ============================================================================
@app.route("/admin/team", methods=["GET", "POST"])
@admin_required
def admin_team():
    if request.method == "POST":
        names = request.form.getlist("name")
        roles = request.form.getlist("role")
        new_team = []
        for i in range(len(names)):
            if names[i].strip():
                new_team.append({
                    "id": f"team-{i+1}",
                    "name": names[i].strip(),
                    "role": roles[i].strip() if i < len(roles) else "",
                })
        db.save_team(new_team)
        flash("টিম মেম্বার তালিকা সফলভাবে সংরক্ষিত হয়েছে!")
        return redirect(url_for("admin_team"))

    team = db.get_team()
    return render_template("admin/team.html", active_page="team", team=team)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
