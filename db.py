import json
import os
import shutil
import uuid
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_FILE = os.path.join(DATA_DIR, "db.json")

DEFAULT_SETTINGS = {
    # Site & Brand
    "site_title": "পড়ারঘর — সহজ ভাষায় ক্যারিয়ার স্কিল প্ল্যাটফর্ম",
    "brand_name": "পড়ারঘর",
    "brand_tagline": "সহজ ভাষায় কাজের স্কিল",
    "brand_logo_text": "প",
    "search_placeholder": "কোর্স বা স্কিল খুঁজুন...",
    "nav_cta_text": "লগইন / সাইন আপ",
    "nav_cta_link": "/login",

    # Announcement / Offer Bar
    "announcement": "🔥 নতুন ব্যাচে ভর্তি চলছে! ২৫ অক্টোবর পর্যন্ত ৫০% বিশেষ ছাড়",
    "announcement_badge": "অফার",
    "announcement_active": True,
    "announcement_link": "/courses",

    # Contact & Helpline
    "phone": "০১৭১১-৬৬২২৪৪",
    "phone_hours": "সকাল ১০টা - রাত ৯টা",
    "email": "support@porarghor.com",
    "address": "বাড়ি ১৮, নুরজাহান রোড, মোহাম্মদপুর, ঢাকা ১২০৭, বাংলাদেশ।",
    "studio_help_title": "ছাত্র-ছাত্রীদের সহায়তা",
    "studio_help_desc": "প্রতি শুক্রবার সরাসরি স্টুডিওতে প্র্যাকটিস সেশন।",
    "footer_about": "সহজ বাংলায় ক্যারিয়ার ও ফ্রিল্যান্সিং স্কিল ডেভেলপমেন্টের বিশ্বস্ত প্ল্যাটফর্ম। কোনো মুখস্থ বা ফাঁকা বুলি নয় — সরাসরি প্র্যাকটিক্যাল প্রজেক্ট আর লাইভ সাপোর্টে ক্যারিয়ার গড়ুন।",
    "footer_copyright": "পড়ারঘর (PorarGhor). সর্বস্বত্ব সংরক্ষিত।",
    "footer_sub_copyright": "সহজ বাংলায় বাস্তবমুখী ক্যারিয়ার স্কিল প্ল্যাটফর্ম",

    # Hero Section
    "hero_pill": "✨ ২৫,০০০+ শিক্ষার্থীর ক্যারিয়ার গড়ার বিশ্বস্ত প্ল্যাটফর্ম",
    "hero_title": "সহজ বাংলায় কাজের স্কিল শিখুন, এগিয়ে থাকুন ক্যারিয়ারে!",
    "hero_desc": "ইউটিউবের টিউটোরিয়াল দেখে আটকে যান? এখানে পাবেন বাস্তব ফাইল, নোংরা ডেটা পরিষ্কার করার আসল নিয়ম, এবং প্রতি সপ্তাহে অভিজ্ঞ মেন্টরের লাইভ প্রশ্নোত্তর সাপোর্ট।",
    "hero_btn1_text": "কোর্সগুলো দেখুন",
    "hero_btn1_link": "/courses",
    "hero_btn2_text": "আসন্ন লাইভ ওয়ার্কশপ",
    "hero_btn2_link": "/workshops",
    "hero_image": "/static/images/hero.jpg",
    "hero_stat_students": "২৫,০০০+",
    "hero_stat_students_label": "সক্রিয় শিক্ষার্থী",
    "hero_stat_rating": "৪.৯ ★",
    "hero_stat_rating_label": "গড় রেটিং (১,২০০+ রিভিউ)",
    "hero_stat_projects": "১০০%",
    "hero_stat_projects_label": "হাতে-কলমে প্রজেক্ট",
    "hero_float1_title": "লাইভ মেন্টরশিপ সাপোর্ট",
    "hero_float1_desc": "সরাসরি মেন্টরের সাথে প্রশ্ন-উত্তর",
    "hero_float2_title": "যাচাইকৃত সার্টিফিকেট",
    "hero_float2_desc": "ক্যারিয়ার প্রোফাইলে যুক্ত করার মতো",

    # Section Headings
    "courses_tag": "সেরা কোর্সসমূহ",
    "courses_title": "জনপ্রিয় ও প্র্যাকটিক্যাল কোর্স",
    "courses_desc": "চাকরি ও ফ্রিল্যান্সিংয়ে সবচেয়ে বেশি প্রয়োজন হয় এমন দক্ষতার কোর্সগুলো বেছে নিন",

    "workshops_tag": "ইন্টারেক্টিভ লার্নিং",
    "workshops_title": "আসন্ন লাইভ ওয়ার্কশপ",
    "workshops_desc": "সরাসরি মেন্টরের সাথে বসে ৩ ঘণ্টায় হাতে-কলমে একটা প্রজেক্ট শেষ করুন",

    "features_tag": "পড়ারঘরের বৈশিষ্ট্য",
    "features_title": "কেন হাজারো তরুণ-তরুণী আমাদের ওপর আস্থা রাখছেন?",
    "features_desc": "আমরা কোনো জটিল থিওরি বা অপ্রয়োজনীয় সিলেবাস করাই না। যেটুকু জানলে সরাসরি কাজ পাওয়া যায়, সেটুকুই শেখাই।",

    "blog_tag": "নলেজ হাব",
    "blog_title": "ক্যারিয়ার টিপস ও গাইডলাইন",
    "blog_desc": "চাকরি ও ফ্রিল্যান্সিংয়ে প্রতিদিনের সাধারণ ভুলগুলো শুধরে নেওয়ার জরুরি পরামর্শ",

}

DEFAULT_NAV = [
    {"endpoint": "index", "label": "হোম", "url": "/"},
    {"endpoint": "courses", "label": "কোর্স", "url": "/courses"},
    {"endpoint": "bundles", "label": "বান্ডেল", "url": "/bundles"},
    {"endpoint": "workshops", "label": "ওয়ার্কশপ", "url": "/workshops"},
    {"endpoint": "ebooks", "label": "ই-বুক", "url": "/ebooks"},
    {"endpoint": "blog", "label": "খবর", "url": "/blog"},
]

DEFAULT_COURSES = [
    {
        "id": "excel-office",
        "title": "অফিস এক্সেল: চাকরির হিসাব থেকে রিপোর্ট",
        "short": "পিভট, ভিলুকআপ, ড্যাশবোর্ড — অফিসে যা লাগে, তা-ই।",
        "category": "অফিস",
        "level": "শুরুর দিক",
        "hours": 18,
        "lessons": 42,
        "price": 1490,
        "old": 2490,
        "instructor": "ফারহানা আক্তার",
        "role": "অডিট ফার্মে ৯ বছর",
        "students": 2140,
        "rating": 4.9,
        "reviews": 184,
        "badge": "চাকরির জন্য",
        "tag": "বেস্টসেলার",
        "image": "/static/images/courses/excel-office.jpg",
        "modules": [
            "সেল, শিট, প্রিন্ট সেটআপ — নোংরা ফাইল পরিষ্কার",
            "সূত্র: IF, SUMIFS, TEXT, DATE",
            "VLOOKUP / XLOOKUP, Pivot টেবিল",
            "ম্যানেজারের জন্য এক পাতার ড্যাশবোর্ড",
        ],
    },
    {
        "id": "spoken-desk",
        "title": "কাজের ইংরেজি: মিটিং, ইমেইল, ক্লায়েন্ট কল",
        "short": "গ্রামার ক্লাস না। যে বাক্যগুলো প্রতিদিন লাগে।",
        "category": "ইংরেজি",
        "level": "মাঝারি",
        "hours": 14,
        "lessons": 36,
        "price": 1790,
        "old": 2990,
        "instructor": "রাফিউল হাসান",
        "role": "ঢাকায় BPO টিম লিড",
        "students": 1860,
        "rating": 4.8,
        "reviews": 126,
        "badge": "কথা বলার",
        "tag": "জনপ্রিয়",
        "image": "/static/images/courses/spoken-desk.jpg",
        "modules": [
            "ইমেইল খোলা-বন্ধা, ফলোআপ, না বলা",
            "জুম কলে বাধা দেওয়া / সময় চাওয়া",
            "ক্লায়েন্ট রেট নিয়ে কথা",
            "ছোট প্রেজেন্টেশন: ৬ স্লাইড রুল",
        ],
    },
    {
        "id": "video-cut",
        "title": "রিলস ও ইউটিউব কাট: ফোন + প্রিমিয়ার",
        "short": "দোকান, কোচিং, পেজ — ভিডিও বিক্রি করে এমন মানুষের জন্য।",
        "category": "ভিডিও",
        "level": "শুরুর দিক",
        "hours": 22,
        "lessons": 51,
        "price": 2190,
        "old": 3990,
        "instructor": "নাফিসা চৌধুরী",
        "role": "ফ্রিল্যান্স এডিটর, চট্টগ্রাম",
        "students": 980,
        "rating": 4.9,
        "reviews": 92,
        "badge": "ফ্রিল্যান্স",
        "tag": "ট্রেন্ডিং",
        "image": "/static/images/courses/video-cut.jpg",
        "modules": [
            "ফোনে শুটিং: আলো, অডিও, হাত কাঁপা",
            "কাট, ক্যাপশন, হুক — ১৫ সেকেন্ড",
            "প্রিমিয়ারে কালার ও সাউন্ড",
            "ক্লায়েন্টকে ফোল্ডার দিয়ে ডেলিভারি",
        ],
    },
    {
        "id": "shop-ads",
        "title": "ফেসবুক অ্যাডস: লোকাল দোকান ও কোচিং",
        "short": "বড় এজেন্সির কেস স্টাডি না। উত্তরা, সিলেট, বগুড়ার বাজেট।",
        "category": "মার্কেটিং",
        "level": "মাঝারি",
        "hours": 16,
        "lessons": 29,
        "price": 1990,
        "old": 3200,
        "instructor": "তানভীর মাহমুদ",
        "role": "দোকান পেজ চালান, নিজেই",
        "students": 1544,
        "rating": 4.8,
        "reviews": 115,
        "badge": "বিক্রি",
        "tag": "হাতে-কলমে",
        "image": "/static/images/courses/shop-ads.jpg",
        "modules": [
            "পিক্সেল, ক্যাটালগ, হোয়াটসঅ্যাপ ক্লিক",
            "৩০০০ টাকার ক্যাম্পেইন গুছিয়ে চালানো",
            "ক্রিয়েটিভ: যা ছবি তুলবেন দোকান থেকে",
            "কী দেখবেন ৭ দিন পর — থামবেন কখন",
        ],
    },
    {
        "id": "canva-print",
        "title": "ক্যানভা: পোস্টার, মেনু, সার্টিফিকেট",
        "short": "প্রিন্ট শপের কাজ ঘরে বসে।",
        "category": "ডিজাইন",
        "level": "শুরুর দিক",
        "hours": 10,
        "lessons": 24,
        "price": 990,
        "old": 1600,
        "instructor": "মিম খাতুন",
        "role": "প্রিন্ট হাউস, মিরপুর",
        "students": 3012,
        "rating": 5.0,
        "reviews": 320,
        "badge": "হাতে-কলমে",
        "tag": "সবচেয়ে সহজ",
        "image": "/static/images/courses/canva-print.jpg",
        "modules": [
            "সাইজ, ব্লিড, রঙ — প্রিন্টারে যা যায়",
            "মেনু, প্রাইস লিস্ট, ঈদ পোস্টার",
            "সার্টিফিকেট ও আইডি কার্ড",
            "ক্লায়েন্টকে PDF/PNG পাঠানো",
        ],
    },
    {
        "id": "web-start",
        "title": "ওয়েবের হিসাব: HTML, CSS, একটা ল্যান্ডিং",
        "short": "ফ্রেমওয়ার্ক নয়। একটা পেজ নিজে শেষ করা।",
        "category": "ওয়েব",
        "level": "শুরুর দিক",
        "hours": 28,
        "lessons": 60,
        "price": 2490,
        "old": 4500,
        "instructor": "সাইফুল ইসলাম",
        "role": "এজেন্সি ডেভ, খুলনা",
        "students": 670,
        "rating": 4.9,
        "reviews": 68,
        "badge": "ধৈর্য লাগে",
        "tag": "ক্যারিয়ার ট্র্যাক",
        "image": "/static/images/courses/web-start.jpg",
        "modules": [
            "ফোল্ডার, ফাইল, ব্রাউজার",
            "লেআউট: ফ্লেক্স, না গ্রিড — কখন কোনটা",
            "ফর্ম, মোবাইল, ছবি চেপে রাখা",
            "Netlify-তে তুলে ক্লায়েন্টকে লিংক",
        ],
    },
]

DEFAULT_BUNDLES = [
    {
        "id": "office-pack",
        "title": "অফিস প্যাক",
        "price": 2890,
        "old": 4280,
        "includes": ["excel-office", "spoken-desk", "canva-print"],
        "note": "চাকরির ইন্টারভিউয়ের আগে তিন মাস।",
    },
    {
        "id": "page-pack",
        "title": "পেজ ও ভিডিও প্যাক",
        "price": 3590,
        "old": 6180,
        "includes": ["shop-ads", "video-cut", "canva-print"],
        "note": "দোকান/কোচিং পেজ যারা একা চালান।",
    },
]

DEFAULT_WORKSHOPS = [
    {
        "id": "wk-cv",
        "title": "শনিবার: সিভি কাটা ও লিংকডইন",
        "when": "২৫ অক্টোবর, সকাল ১০টা",
        "place": "মোহাম্মদপুর স্টুডিও + জুম",
        "seats": "১৪ সিট বাকি",
        "price": 450,
    },
    {
        "id": "wk-rate",
        "title": "ফ্রিল্যান্স রেট কীভাবে বলবেন",
        "when": "১ নভেম্বর, রাত ৮টা",
        "place": "শুধু জুম",
        "seats": "অনলাইন, সীমা ৪০",
        "price": 300,
    },
    {
        "id": "wk-tax",
        "title": "ফ্রিল্যান্সারের TIN ও ইনভয়েস",
        "when": "৮ নভেম্বর, বিকাল ৪টা",
        "place": "মোহাম্মদপুর স্টুডিও",
        "seats": "৮ সিট বাকি",
        "price": 500,
    },
]

DEFAULT_EBOOKS = [
    {
        "id": "eb-email",
        "title": "৪০টা ইমেইল টেমপ্লেট",
        "pages": 38,
        "price": 190,
    },
    {
        "id": "eb-rate",
        "title": "রেট কার্ড: ভিডিও ও ক্যানভা",
        "pages": 12,
        "price": 120,
    },
    {
        "id": "eb-excel",
        "title": "এক্সেল সূত্র খাতা",
        "pages": 54,
        "price": 250,
    },
]

DEFAULT_POSTS = [
    {
        "id": "cv-one-page",
        "title": "সিভি এক পাতাই রাখুন, দুই পাতা নয়",
        "date": "৩ অক্টোবর ২০২৬",
        "tag": "চাকরি",
        "body": "ম্যানেজার ৮ সেকেন্ড দেখেন। স্কিল উপরে, দায়িত্ব বুলেট, লিংক নিচে। ছবি বাদ দিন যদি জব সার্কুলেশন না চায়।",
    },
    {
        "id": "bkash-ad",
        "title": "অ্যাডস বাজেট শেষ হয়ে গেলে যা করবেন না",
        "date": "২৮ সেপ্টেম্বর ২০২৬",
        "tag": "পেজ",
        "body": "লক্ষ্য বদলে নতুন ক্যাম্পেইন ঝাঁপিয়ে পড়া মানে আগের লার্নিং ফেলা। দুই দিন অপেক্ষা, ক্রিয়েটিভ বদলান, অডিয়েন্স নয়।",
    },
    {
        "id": "night-class",
        "title": "রাতের ব্যাচ যাদের চাকরি আছে",
        "date": "১২ সেপ্টেম্বর ২০২৬",
        "tag": "পড়ারঘর",
        "body": "আমরা রাত ৯টায় ক্লাস রাখি কারণ সকালের ব্যাচ অফিস যায় না, যায় না বলে মিথ্যা বলা বন্ধ করতে।",
    },
]

DEFAULT_CERTS = {
    "PG-4821": {"name": "সাদিয়া রহমান", "course": "অফিস এক্সেল", "date": "আগস্ট ২০২৬"},
    "PG-1109": {"name": "ইমরান হোসেন", "course": "কাজের ইংরেজি", "date": "জুলাই ২০২৬"},
}

DEFAULT_TEAM = [
    {"id": "team-1", "name": "ফারহানা আক্তার", "role": "এক্সেল ও অডিট"},
    {"id": "team-2", "name": "রাফিউল হাসান", "role": "ইংরেজি ডেস্ক"},
    {"id": "team-3", "name": "নাফিসা চৌধুরী", "role": "ভিডিও"},
    {"id": "team-4", "name": "তানভীর মাহমুদ", "role": "অ্যাডস"},
]

DEFAULT_TRUST = [
    {"icon": "file", "title": "বাস্তব কাজের ফাইল", "desc": "স্লাইড নয়, সরাসরি ক্লাসের এক্সেল ও টেমপ্লেট"},
    {"icon": "clock", "title": "লাইফটাইম অ্যাক্সেস", "desc": "যেকোনো সময় যেকোনো ডিভাইস থেকে দেখার সুবিধা"},
    {"icon": "users", "title": "ডেডিকেটেড স্টুডেন্ট গ্রুপ", "desc": "হোয়াটসঅ্যাপ ও ফেসবুক প্রাইভেট কমিউনিটি"},
    {"icon": "star", "title": "দক্ষ ইন্সট্রাক্টর", "desc": "ফিল্ডে কাজ করা অভিজ্ঞ প্রফেশনালদের কোর্স"}
]

DEFAULT_FEATURES = [
    {"title": "স্লাইড নয়, সরাসরি আসল ফাইল", "desc": "আমরা জটিল পাওয়ারপয়েন্ট স্লাইড বানিয়ে সময় নষ্ট করি না। ক্লাসে যে ফাইল ওপেন করা হয়, সেটাই সরাসরি স্টুডেন্টদের ডাউনলোড করতে দেওয়া হয়।"},
    {"title": "সহজ মাতৃভাষা বাংলায় ব্যাখ্যা", "desc": "কঠিন ইংরেজি টার্ম মুখস্থ করার ভয় নেই। বাংলায় সহজভাবে বুঝিয়ে দেওয়া হয়, সাথে প্রফেশনাল শব্দগুলো ব্যবহারের সঠিক নিয়ম শেখানো হয়।"},
    {"title": "ছোট ব্যাচে নিবিড় সাপোর্ট", "desc": "প্রতিটি শিক্ষার্থীর অ্যাসাইনমেন্ট আলাদাভাবে চেক করা হয় এবং সপ্তাহে লাইভে মেন্টরের সাথে সরাসরি প্রশ্ন করার পূর্ণ সুযোগ থাকে।"}
]

DEFAULT_LEGAL = {
    "terms": {
        "title": "ব্যবহারের শর্তাবলী",
        "content": "<p><strong>১. ব্যক্তিগত ব্যবহারের নিয়ম:</strong> পড়ারঘরের সমস্ত কোর্স ও কন্টেন্ট শুধুমাত্র আপনার নিজস্ব ক্যারিয়ার উন্নয়নের জন্য। কোনো কোর্স ভিডিও বা রিসোর্স অন্য কারো সাথে শেয়ার করা বা সোশ্যাল মিডিয়ায় আপলোড করা সম্পূর্ণ নিষিদ্ধ।</p><p><strong>২. অ্যাকাউন্ট সিকিউরিটি:</strong> একটি অ্যাকাউন্ট একই সময়ে একাধিক ডিভাইসে শেয়ার করলে সিস্টেম স্বয়ংক্রিয়ভাবে অ্যাকাউন্ট সাময়িক স্থগিত করতে পারে।</p>"
    },
    "privacy": {
        "title": "প্রাইভেসি পলিসি",
        "content": "<p><strong>১. তথ্যের গোপনীয়তা:</strong> আপনার নাম, ফোন নম্বর ও ইমেইল শুধুমাত্র কোর্স অ্যাক্সেস ও গুরুত্বপূর্ণ ক্লাস নোটিফিকেশনের জন্য ব্যবহৃত হয়। আমরা কখনোই কোনো তৃতীয় পক্ষের কাছে আপনার তথ্য বিক্রি করি না।</p><p><strong>২. পেমেন্ট নিরাপত্তা:</strong> পেমেন্ট লেনদেন সরাসরি দেশের সিকিউরড পেমেন্ট গেটওয়ে (SSLCommerz/bKash/Nagad) দ্বারা নিয়ন্ত্রিত। আপনার কোনো কার্ড বা গোপন পিন আমাদের সার্ভারে সংরক্ষিত হয় না।</p>"
    },
    "refund": {
        "title": "রিফান্ড নীতি",
        "content": "<p><strong>১. ৭ দিনের মানিব্যাক গ্যারান্টি:</strong> কোর্স কেনার ৭ দিনের মধ্যে যদি কোর্সটি আপনার প্রত্যাশানুযায়ী না হয় এবং আপনি ২০% এর কম ভিডিও দেখে থাকেন, তবে নিঃশর্তে ১০০% টাকা রিফান্ড পেতে পারেন।</p><p><strong>২. ওয়ার্কশপ পলিসি:</strong> লাইভ ওয়ার্কশপের আসন সংখ্যা সীমিত থাকায় ওয়ার্কশপের ক্ষেত্রে কোনো রিফান্ড প্রযোজ্য নয়, তবে আপনি পরবর্তী ব্যাচে ক্লাসটি শিফট করতে পারবেন।</p>"
    }
}

DEFAULT_OFFERS = [
    {
        "id": "off-eid",
        "code": "PORA50",
        "title": "নতুন ব্যাচ স্পেশাল ডিসকাউন্ট",
        "discount_type": "percent", # percent or fixed
        "discount_value": 50,
        "valid_until": "২৫ অক্টোবর ২০২৬",
        "is_active": True,
        "note": "সকল কোর্সে ৫০% ছাড় পেতে চেকআউটে কোডটি ব্যবহার করুন"
    }
]

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DB_FILE):
        data = {
            "settings": DEFAULT_SETTINGS,
            "nav": DEFAULT_NAV,
            "courses": DEFAULT_COURSES,
            "workshops": DEFAULT_WORKSHOPS,
            "bundles": DEFAULT_BUNDLES,
            "ebooks": DEFAULT_EBOOKS,
            "posts": DEFAULT_POSTS,
            "certs": DEFAULT_CERTS,
            "team": DEFAULT_TEAM,
            "trust": DEFAULT_TRUST,
            "features": DEFAULT_FEATURES,
            "legal": DEFAULT_LEGAL,
            "offers": DEFAULT_OFFERS,
            "messages": [],
            "enrollments": [],
            "students": [],
            "orders": [],
            "payments": [],
            "progress": []
        }
        save_db(data)
        return data
    return load_db()

def load_db():
    if not os.path.exists(DB_FILE):
        return init_db()
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure defaults for newly added keys
            dirty = False
            settings = data.setdefault("settings", {})
            for key in ("admin_username", "admin_password"):
                if key in settings:
                    del settings[key]
                    dirty = True
            for k, v in DEFAULT_SETTINGS.items():
                if k not in settings:
                    settings[k] = v
                    dirty = True
            for col, val in [
                ("nav", DEFAULT_NAV),
                ("courses", DEFAULT_COURSES),
                ("workshops", DEFAULT_WORKSHOPS),
                ("bundles", DEFAULT_BUNDLES),
                ("ebooks", DEFAULT_EBOOKS),
                ("posts", DEFAULT_POSTS),
                ("certs", DEFAULT_CERTS),
                ("team", DEFAULT_TEAM),
                ("trust", DEFAULT_TRUST),
                ("features", DEFAULT_FEATURES),
                ("legal", DEFAULT_LEGAL),
                ("offers", DEFAULT_OFFERS),
                ("messages", []),
                ("enrollments", []),
                ("students", []),
                ("orders", []),
                ("payments", []),
                ("progress", [])
            ]:
                if col not in data:
                    data[col] = val
                    dirty = True
            if dirty:
                save_db(data)
            return data
    except Exception:
        return init_db()

def save_db(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    temp_file = DB_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    shutil.move(temp_file, DB_FILE)

# Helper functions
def get_settings():
    return load_db().get("settings", DEFAULT_SETTINGS)

def update_settings(new_settings):
    db = load_db()
    current = db.get("settings", DEFAULT_SETTINGS)
    current.update(new_settings)
    db["settings"] = current
    save_db(db)
    return db["settings"]

def get_nav():
    return load_db().get("nav", DEFAULT_NAV)

def save_nav(nav_list):
    db = load_db()
    db["nav"] = nav_list
    save_db(db)

def get_courses():
    return load_db().get("courses", [])

def get_course(cid):
    for c in get_courses():
        if c.get("id") == cid:
            return c
    return None

def save_course(course_data, is_new=False):
    db = load_db()
    courses = db.get("courses", [])
    if is_new:
        # Check if ID already exists
        courses = [c for c in courses if c.get("id") != course_data.get("id")]
        courses.append(course_data)
    else:
        for idx, c in enumerate(courses):
            if c.get("id") == course_data.get("id"):
                courses[idx] = course_data
                break
        else:
            courses.append(course_data)
    db["courses"] = courses
    save_db(db)

def delete_course(cid):
    db = load_db()
    db["courses"] = [c for c in db.get("courses", []) if c.get("id") != cid]
    save_db(db)

def get_workshops():
    return load_db().get("workshops", [])

def save_workshop(w_data, is_new=False):
    db = load_db()
    workshops = db.get("workshops", [])
    if is_new:
        workshops = [w for w in workshops if w.get("id") != w_data.get("id")]
        workshops.append(w_data)
    else:
        for idx, w in enumerate(workshops):
            if w.get("id") == w_data.get("id"):
                workshops[idx] = w_data
                break
        else:
            workshops.append(w_data)
    db["workshops"] = workshops
    save_db(db)

def delete_workshop(wid):
    db = load_db()
    db["workshops"] = [w for w in db.get("workshops", []) if w.get("id") != wid]
    save_db(db)

def get_bundles():
    return load_db().get("bundles", [])

def save_bundle(b_data, is_new=False):
    db = load_db()
    bundles = db.get("bundles", [])
    if is_new:
        bundles = [b for b in bundles if b.get("id") != b_data.get("id")]
        bundles.append(b_data)
    else:
        for idx, b in enumerate(bundles):
            if b.get("id") == b_data.get("id"):
                bundles[idx] = b_data
                break
        else:
            bundles.append(b_data)
    db["bundles"] = bundles
    save_db(db)

def delete_bundle(bid):
    db = load_db()
    db["bundles"] = [b for b in db.get("bundles", []) if b.get("id") != bid]
    save_db(db)

def get_ebooks():
    return load_db().get("ebooks", [])

def save_ebook(eb_data, is_new=False):
    db = load_db()
    ebooks = db.get("ebooks", [])
    if is_new:
        ebooks = [eb for eb in ebooks if eb.get("id") != eb_data.get("id")]
        ebooks.append(eb_data)
    else:
        for idx, eb in enumerate(ebooks):
            if eb.get("id") == eb_data.get("id"):
                ebooks[idx] = eb_data
                break
        else:
            ebooks.append(eb_data)
    db["ebooks"] = ebooks
    save_db(db)

def delete_ebook(ebid):
    db = load_db()
    db["ebooks"] = [eb for eb in db.get("ebooks", []) if eb.get("id") != ebid]
    save_db(db)

def get_posts():
    return load_db().get("posts", [])

def save_post(p_data, is_new=False):
    db = load_db()
    posts = db.get("posts", [])
    if is_new:
        posts = [p for p in posts if p.get("id") != p_data.get("id")]
        posts.insert(0, p_data)
    else:
        for idx, p in enumerate(posts):
            if p.get("id") == p_data.get("id"):
                posts[idx] = p_data
                break
        else:
            posts.append(p_data)
    db["posts"] = posts
    save_db(db)

def delete_post(pid):
    db = load_db()
    db["posts"] = [p for p in db.get("posts", []) if p.get("id") != pid]
    save_db(db)

def get_certs():
    return load_db().get("certs", {})

def save_cert(code, cert_info):
    db = load_db()
    certs = db.get("certs", {})
    certs[code.strip().upper()] = cert_info
    db["certs"] = certs
    save_db(db)

def delete_cert(code):
    db = load_db()
    certs = db.get("certs", {})
    code_up = code.strip().upper()
    if code_up in certs:
        del certs[code_up]
    db["certs"] = certs
    save_db(db)

def get_team():
    return load_db().get("team", DEFAULT_TEAM)

def save_team(team_list):
    db = load_db()
    db["team"] = team_list
    save_db(db)

def get_trust():
    return load_db().get("trust", DEFAULT_TRUST)

def save_trust(trust_list):
    db = load_db()
    db["trust"] = trust_list
    save_db(db)

def get_features():
    return load_db().get("features", DEFAULT_FEATURES)

def save_features(feat_list):
    db = load_db()
    db["features"] = feat_list
    save_db(db)

def get_legal():
    return load_db().get("legal", DEFAULT_LEGAL)

def save_legal(legal_dict):
    db = load_db()
    db["legal"] = legal_dict
    save_db(db)

def get_offers():
    return load_db().get("offers", DEFAULT_OFFERS)

def save_offer(offer_data, is_new=False):
    db = load_db()
    offers = db.get("offers", [])
    if is_new:
        offers = [o for o in offers if o.get("id") != offer_data.get("id")]
        offers.append(offer_data)
    else:
        for idx, o in enumerate(offers):
            if o.get("id") == offer_data.get("id"):
                offers[idx] = offer_data
                break
        else:
            offers.append(offer_data)
    db["offers"] = offers
    save_db(db)

def delete_offer(oid):
    db = load_db()
    db["offers"] = [o for o in db.get("offers", []) if o.get("id") != oid]
    save_db(db)

def add_message(msg):
    db = load_db()
    messages = db.get("messages", [])
    if "id" not in msg:
        msg["id"] = str(uuid.uuid4())[:8]
    if "created_at" not in msg:
        msg["created_at"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
    messages.insert(0, msg)
    db["messages"] = messages
    save_db(db)

def get_messages():
    return load_db().get("messages", [])

def delete_message(mid):
    db = load_db()
    db["messages"] = [m for m in db.get("messages", []) if m.get("id") != mid]
    save_db(db)

def add_enrollment(enrollment):
    db = load_db()
    enrollments = db.get("enrollments", [])
    if "id" not in enrollment:
        enrollment["id"] = str(uuid.uuid4())[:8]
    if "created_at" not in enrollment:
        enrollment["created_at"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
    enrollments.insert(0, enrollment)
    db["enrollments"] = enrollments
    save_db(db)

def get_enrollments():
    return load_db().get("enrollments", [])


def get_students():
    return load_db().get("students", [])


def get_student(student_id):
    for s in get_students():
        if s.get("id") == student_id:
            return s
    return None


def find_student_by_phone(phone):
    p = (phone or "").strip()
    for s in get_students():
        if s.get("phone", "").strip() == p:
            return s
    return None


def save_student(student_data):
    db = load_db()
    students = db.get("students", [])
    sid = student_data.get("id")
    if not sid:
        sid = str(uuid.uuid4())[:8]
        student_data["id"] = sid
    if "created_at" not in student_data:
        student_data["created_at"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
    for idx, s in enumerate(students):
        if s.get("id") == sid:
            students[idx] = {**s, **student_data}
            db["students"] = students
            save_db(db)
            return students[idx]
    students.insert(0, student_data)
    db["students"] = students
    save_db(db)
    return student_data


def add_order(order):
    db = load_db()
    orders = db.get("orders", [])
    if "id" not in order:
        order["id"] = str(uuid.uuid4())[:8]
    if "created_at" not in order:
        order["created_at"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
    orders.insert(0, order)
    db["orders"] = orders
    save_db(db)
    return order


def get_orders_for_student(student_id):
    return [o for o in load_db().get("orders", []) if o.get("student_id") == student_id]


def add_payment(payment):
    db = load_db()
    payments = db.get("payments", [])
    if "id" not in payment:
        payment["id"] = str(uuid.uuid4())[:8]
    if "created_at" not in payment:
        payment["created_at"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
    payments.insert(0, payment)
    db["payments"] = payments
    save_db(db)
    return payment


def get_payments_for_student(student_id):
    return [p for p in load_db().get("payments", []) if p.get("student_id") == student_id]


def save_course_progress(student_id, course_id, payload):
    db = load_db()
    progress_items = db.get("progress", [])
    percent = int(payload.get("percent", 0) or 0)
    watched_seconds = int(payload.get("watched_seconds", 0) or 0)
    record = None
    for item in progress_items:
        if item.get("student_id") == student_id and item.get("course_id") == course_id:
            record = item
            break
    if not record:
        record = {
            "id": str(uuid.uuid4())[:8],
            "student_id": student_id,
            "course_id": course_id,
            "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        }
        progress_items.insert(0, record)
    record["percent"] = max(0, min(100, percent))
    record["watched_seconds"] = max(0, watched_seconds)
    record["updated_at"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
    if record["percent"] >= 100:
        record["status"] = "completed"
    elif record["percent"] > 0:
        record["status"] = "in_progress"
    else:
        record["status"] = "not_started"
    db["progress"] = progress_items
    save_db(db)
    return record


def get_student_course_progress(student_id, course_id):
    for item in load_db().get("progress", []):
        if item.get("student_id") == student_id and item.get("course_id") == course_id:
            return item
    return {"percent": 0, "watched_seconds": 0, "status": "not_started"}


def get_student_progress(student_id):
    return [p for p in load_db().get("progress", []) if p.get("student_id") == student_id]


def delete_enrollment(eid):
    db = load_db()
    db["enrollments"] = [e for e in db.get("enrollments", []) if e.get("id") != eid]
    save_db(db)
