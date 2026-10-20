# Design brief: Bangla-first career LMS

**Purpose:** Original product design notes for a Bangladesh career-skills learning platform in this workspace.  
**Not included:** HTML/CSS/JS, assets, or a pixel clone of any live site.

**Sources:** Public information architecture and marketing chrome from [learningbangladesh.com](https://www.learningbangladesh.com/) (homepage nav/footer, contact, blogs empty state). The live homepage is a client-rendered app, so visual tokens below are **recommendations**, not extracted stylesheets.

---

## 1. Product positioning

- **Audience:** Bangla-speaking learners who want job-oriented skills (courses, bundles, workshops, e-books).
- **Promise:** Career skill development in simple language.
- **Trust signals:** Local phone, email, Dhaka office, trade license, app store, payment logos, certificate verification.
- **Tone:** Friendly, practical, Bangla-first UI with English legal/company pages where needed.

---

## 2. Information architecture

### Primary nav (learner)

| Label (BN) | Role |
|---|---|
| হোম | Landing |
| কোর্স | Course catalog |
| বান্ডেল | Multi-course packages |
| ওয়ার্কশপ | Live / scheduled events |
| ই-বুক | Digital books |
| ব্লগ | Articles |
| সাইন আপ / লগইন | Auth (single control until signed in) |

### Company / conversion (footer & secondary)

- About, team, student success, become an instructor, affiliate, contact
- Catalog mirrors: courses, bundles, services, e-books, blogs
- **Verify certificate** (post-purchase trust)
- Legal: terms, privacy, refund

### Catalog objects

Treat these as first-class entities with shared card UI:

1. **Course** — sequential lessons, price, instructor, duration
2. **Bundle** — grouped courses, savings vs à la carte
3. **Workshop** — date/time, seat limit, live vs recorded
4. **E-book** — file/download or in-app reader
5. **Blog post** — SEO/content; empty state when none match filters

### Auth & learner app (implied, not fully visible without login)

- Register / login
- My learning (enrolled items, progress)
- Checkout (local payment methods)
- Profile, certificates
- Instructor / affiliate applications (forms, not full CMS in the public shell)

---

## 3. Page inventory (public)

| Route intent | Layout | Notes |
|---|---|---|
| Home | Marketing: hero, featured catalog, trust, CTA | SPA; content hydrates in browser |
| Course listing | Filter + grid of cards | Primary conversion |
| Course detail | Hero, syllabus, instructor, price, enroll | |
| Bundle / workshop / e-book listing & detail | Same card system, different badges | |
| Blog index | Search/filters + list | Empty: “no posts matching filters” |
| About / team / success / instructor / affiliate | Long-form + CTA | |
| Contact | Split: copy + form \| office / email / phone | Headline pattern: conversation + form |
| Legal | Dense text, Bangla or EN | |
| Verify certificate | Simple form: code → result | |
| Auth | Modal or dedicated page | Keep in nav on every breakpoint |

---

## 4. Layout system

### Desktop

```
┌─────────────────────────────────────────────────────────┐
│ Utility: phone · email                         (optional)│
├─────────────────────────────────────────────────────────┤
│ Logo    হোম  কোর্স  বান্ডেল  ওয়ার্কশপ  ই-বুক  ব্লগ   [Auth] │
├─────────────────────────────────────────────────────────┤
│                         PAGE                            │
│  max-width ~1200–1280px, 16–24px gutters                │
├─────────────────────────────────────────────────────────┤
│ Footer: brand · Explore · Support · contact · payments  │
└─────────────────────────────────────────────────────────┘
```

- Sticky header; auth always visible.
- Home hero: full-width media or illustration, Bangla H1, primary CTA (browse courses) + secondary (sign up).
- Catalog: 3–4 columns of cards; sidebar or top chips for category, price, level.
- Detail: 2 columns — content left (~65%), sticky buy card right (~35%).
- Contact: 2 columns — form left, contact cards right.

### Mobile

- Hamburger for primary nav (“Open main menu”).
- Auth in header or first menu item.
- Cards: 1 column.
- Sticky bottom CTA on product detail (price + enroll).
- Footer accordion for Explore / Support.

### Loading

Public site shows a Bangla loading state (`লোড হচ্ছে...`). Use a skeleton for catalog grids, not a blank page.

---

## 5. Visual language (recommended tokens)

Use a **green / growth** palette common to Bangladesh edtech, high contrast for Bangla text, plenty of white space.

| Token | Value | Use |
|---|---|---|
| `--color-bg` | `#F7F8F5` | Page |
| `--color-surface` | `#FFFFFF` | Cards, header |
| `--color-text` | `#12261C` | Body |
| `--color-muted` | `#5C6B63` | Meta, captions |
| `--color-primary` | `#0F7B4A` | Buttons, links, progress |
| `--color-primary-hover` | `#0C643C` | Hover |
| `--color-accent` | `#E8B84A` | Sale badges, ratings |
| `--color-danger` | `#C0392B` | Errors, refunds |
| `--color-border` | `#E2E8E4` | Dividers |
| `--radius-card` | `16px` | Cards |
| `--radius-btn` | `10px` | Buttons |
| `--shadow-card` | `0 8px 24px rgba(18, 38, 28, 0.06)` | Elevation |

**Type**

- Bangla UI: `Noto Sans Bengali` or `Hind Siliguri`
- Latin / numbers: `Inter` or `Plus Jakarta Sans`
- Scale: 14 / 16 body, 20–24 card titles, 32–40 page titles, 48–56 home H1
- Line-height ≥ 1.7 for Bangla paragraphs

**Imagery**

- Student/instructor photos, course thumbnails 16:9
- Avoid cluttered stock; prefer local context (Dhaka, classroom, laptop)
- Do **not** copy another brand’s logo, photos, or illustrations

---

## 6. Components

### Header

- Logo left (wordmark + mark)
- Center/right nav
- Solid fill button for auth
- Mobile: menu icon; drawer with same links + phone

### Catalog card

- Thumbnail
- Category chip
- Title (2-line clamp)
- Instructor + duration
- Price (strikethrough original if discounted)
- Optional: “bundle” / “workshop” / “e-book” badge
- Entire card clickable

### Buy / enroll card (detail)

- Price
- Primary: Enroll / Add to cart
- Secondary: Add to wishlist
- Includes list (video hours, quizzes, certificate)
- Payment method row (bKash, Nagad, cards, etc. — use official marks only with license)

### Buttons

- Primary: filled green, white text
- Secondary: outline
- Ghost: text-only for tertiary
- Min height 44px (touch)

### Forms

- Labels above fields, Bangla
- Contact: name, email, phone, message
- Auth: phone OTP is common in BD; email+password as fallback
- Inline validation; don’t rely on color alone

### Empty states

- Illustration or icon + short Bangla explanation + reset filters (blogs already use this pattern)

### Footer

- 3–4 columns: brand/address, Explore, Support, contact
- Trade license line (compliance)
- Social: Facebook, LinkedIn, YouTube, Instagram, WhatsApp
- Play Store badge
- Copyright year

### Certificate verify

- Single field + submit
- Success: name, course, date
- Fail: polite error, support phone

---

## 7. Interaction & motion

- Page transitions: none or 150ms fade (SPA feel without waiting spinners on every click)
- Hover on cards: 4px lift, border tint
- Progress bars on “my learning”
- Focus rings: 2px primary outline for keyboard

---

## 8. Key user flows

1. **Discover → enroll:** Home / catalog → detail → auth (if needed) → checkout → my learning  
2. **Bundle:** Bundle detail → checkout (all included courses unlocked)  
3. **Workshop:** Pick date → pay → calendar/WhatsApp confirmation  
4. **E-book:** Pay → download or reader  
5. **Trust:** Verify certificate from footer  
6. **Instructor/affiliate:** Landing → application form → email follow-up  
7. **Support:** Contact form + hotline `09643…` pattern + WhatsApp

---

## 9. Responsive & a11y

- Breakpoints: 360 / 768 / 1024 / 1280
- Bangla truncation: test long titles
- Contrast ≥ WCAG AA on primary buttons
- Skip link, landmark header/main/footer
- Form errors associated with `aria-describedby`

---

## 10. Build this (original stack suggestion)

Not a reconstruction of any vendor’s repo:

- **App:** Next.js (App Router) + TypeScript
- **UI:** Tailwind + headless components (Radix)
- **i18n:** Bangla default, English optional
- **Auth:** Phone OTP + email
- **Payments:** SSLCommerz / bKash / Nagad (server-side only)
- **Media:** HLS for video, signed URLs
- **CMS:** courses/bundles as structured content (not scraped HTML)

---

## 11. Cursor Browser Tab (this machine)

The agent in this chat **does not have** Cursor Browser MCP tools (`browser_navigate`, click, screenshot). Fetching the marketing site only returned shell chrome because the homepage hydrates in the client.

To review the live UI **inside Cursor** yourself:

1. Cursor Settings → **Tools & MCP** → enable **Browser Automation** / **Browser Tab**
2. Command Palette → **Browser: Open Integrated Browser** (or **Simple Browser: Show**)
3. Paste `https://www.learningbangladesh.com/`
4. Optionally `@browser` in Agent chat on a later turn so screenshots can refine this file (colors, spacing, hero)

Until that is enabled, treat §5 as a starting palette and replace tokens after a visual pass.

---

## 12. Out of scope

- Copying or reconstructing another company’s source, minified bundles, or assets
- Reusing their brand name, logo, or trade dress in a competing product
- Scraping course content, student data, or authenticated areas
