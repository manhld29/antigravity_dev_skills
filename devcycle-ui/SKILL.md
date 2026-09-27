---
name: devcycle-ui
description: "UI/UX builder & design intelligence based on NextLevelBuilder UI-UX Pro Max standards + taste-skill (anti-slop) + impeccable (award-winning design director) + emilkowalski/skills (motion & animation). Supports Web (Tailwind, Vanilla CSS, React, Vue, Next.js) and Desktop (PySide6, Qt, QML, QSS). Triggers: \"design UI\", \"build UI\", \"style this window\", \"create component\", \"devcycle-ui\", \"thiết kế giao diện\", \"animate\", \"motion\", \"polish design\", \"impeccable\"."
argument-hint: "What screen, component, or theme to design?"
---

# Devcycle — UI (Universal UI/UX Builder & Design Intelligence)

Provides world-class design systems, component patterns, and visual styling for both
**Web applications** (Tailwind CSS, Vanilla CSS, React, Next.js) and **Desktop apps** (PySide6, Qt, QML, QSS).

Powered by **3 elite external skill packs** installed at system level:

| Pack | Description | Skills available |
|------|-------------|-----------------|
| **taste-skill** (Leonxlnx) | Anti-slop frontend framework | `taste-skill-web`, `brutalist-skill`, `minimalist-skill`, `soft-skill`, `redesign-skill`, `output-skill`, `stitch-skill` |
| **impeccable** (pbakaus) | Award-winning design director AI | `impeccable-design` with commands: craft, shape, audit, polish, bolder, animate, colorize, typeset, layout, delight |
| **emilkowalski/skills** | Motion & animation engineering | `animate`, `review-animations`, `improve-animations`, `find-animation-opportunities`, `animation-vocabulary`, `apple-design`, `pick-ui-library` |

---

## 0. BRIEF INFERENCE (Read the Room First — from taste-skill)

Before touching any code, **infer what the user actually wants**. State a one-line "Design Read":

> **"Reading this as: `<page kind>` for `<audience>`, with a `<vibe>` language, leaning toward `<design system or aesthetic family>`."**

### Anti-Default Discipline
NEVER default to: AI-purple gradients, centered hero over dark mesh, three equal feature cards, generic glassmorphism everywhere, Inter + slate-900. These are LLM defaults. Reach past them based on the design read.

---

## 1. Core Design Aesthetics (Zero-Mediocrity Policy)

1. **Color & Elevation**:
   - Avoid generic base colors (pure red, green, blue). Use curated HSL tokens, sleek dark modes, and subtle gradients.
   - Use Glassmorphism (`backdrop-filter: blur()`) and soft layered drop-shadows where appropriate.
2. **Typography & Hierarchy**:
   - Modern typography (Inter, Plus Jakarta Sans, Outfit, Roboto, custom serifs for editorial).
   - Clear modular scale hierarchy (H1, H2, Body, Small) with intentional leading and tracking.
3. **Dynamic Motion & Micro-Animations**:
   - Apply Emil Kowalski's animation philosophy: animate only what earns it, right curve, right duration.
   - Smooth hover states, active transitions, staggered reveals, spatial consistency.

---

## 2. The Three Dials (from taste-skill)

After the design read, set three dials that gate every layout, motion, and density decision:

- **`DESIGN_VARIANCE: 1-10`** → 1 = Perfect Symmetry, 10 = Artsy Chaos
- **`MOTION_INTENSITY: 1-10`** → 1 = Static, 10 = Cinematic / Physics
- **`VISUAL_DENSITY: 1-10`** → 1 = Art Gallery / Airy, 10 = Cockpit / Packed Data

---

## 3. Design Mode Selection (from impeccable)

Choose the correct mode based on the surface type:

- **Persuade** — Landing pages, marketing, campaigns. Earn attention and action.
- **Operate** — App UI, dashboards, editors, admin. Scanability & consistency over expression.
- **Read** — Docs, articles, guides. Structure for comprehension.
- **Experience** — Portfolios, galleries, showcases. The artifact leads.

---

## 4. Animation Rules (from emilkowalski/skills)

### Should it animate at all?

| Frequency | Decision |
|-----------|----------|
| 100+ times/day (keyboard shortcuts, cmd palette) | **No animation. Ever.** |
| Tens of times/day (hover, list navigation) | Near-imperceptible only |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare / first-time (onboarding, celebration) | The delight budget |

### Animation Hard Rules
1. No `ease-in` on entrances. No `scale(0)`. No keyframes on toasts.
2. Every curve, duration, spring config from established tables — never invent values.
3. Reduced motion gating ships **with** the animation, not as follow-up.
4. Cheapest tool that works. Don't install a library for a fade.

---

## 5. Design Intelligence Knowledge Search (BM25 CLI)

Search the bundled design database without leaving the terminal:

```bash
# 1. Search color palettes
python ~/.gemini/config/skills/devcycle-ui/scripts/search.py "dark modern" --domain color

# 2. Search typography pairings
python ~/.gemini/config/skills/devcycle-ui/scripts/search.py "saas dashboard" --domain typography

# 3. Search UI styles (Glassmorphism, Minimalist, Cyberpunk, Neo-brutalism)
python ~/.gemini/config/skills/devcycle-ui/scripts/search.py "fintech" --domain style

# 4. Generate a complete token-driven design system
python ~/.gemini/config/skills/devcycle-ui/scripts/search.py "modern dark" --design-system -p "MyProject"
```

---

## 6. Skill Delegation Guide

### For anti-slop frontend / landing pages
→ Activate `taste-skill-web` skill for detailed taste enforcement

### For premium award-winning design (full redesign / craft)
→ Activate `impeccable-design` skill
→ Run: `impeccable context` then use commands: `shape`, `craft`, `polish`, `bolder`, `audit`

### For animations & motion engineering
→ Activate `animate` skill (building from scratch)
→ Activate `review-animations` skill (critiquing existing motion)
→ Activate `improve-animations` skill (auditing whole codebase)
→ Activate `find-animation-opportunities` skill (where to add motion)

### For specific aesthetic variants
→ `brutalist-skill` — raw editorial / brutalist design
→ `minimalist-skill` — clean minimal / Linear-style
→ `soft-skill` — warm consumer / premium soft
→ `apple-design` — Apple HIG design language
→ `redesign-skill` — redesigning existing products

---

## 7. Web & Desktop Workflows

### Web Applications (React / Vue / HTML + CSS)
- Define CSS custom properties / Tailwind theme tokens (`--primary`, `--surface`, `--accent`).
- Separate UI view components from state / data-fetching logic.
- Apply taste-skill anti-slop discipline before shipping.
- Run impeccable `audit` + `polish` before final delivery.
- Verify with browser testing and screenshot captures.

### Desktop Applications (PySide6 / Qt)
- Generate `<Screen>.qml` + `<Screen>.qss` token-driven styles.
- Preview and capture headless screenshot:
  ```bash
  python ~/.gemini/config/skills/devcycle-ui/scripts/render_ui.py --qss ui/style.qss --screenshot preview.png
  ```

---

## 8. Quality Gates (before shipping any UI)

1. ✅ Design Read declared and dials set
2. ✅ No LLM-default aesthetics (anti-slop check)
3. ✅ Motion passes Emil Kowalski animation rules
4. ✅ Impeccable craft floor respected (no a11y violations, responsive)
5. ✅ Screenshot captured for visual verification

---

## 9. Liên Kết Toàn Diện Hệ Sinh Thái UI/UX (Comprehensive UI Skill Ecosystem)

| Nhóm Năng Lực | Kỹ Năng Tích Hợp | Vai Trò & Trường Hợp Kích Hoạt |
|---|---|---|
| **Design Core** | [ui-ux-pro-max](../ui-ux-pro-max/SKILL.md) | Chuẩn mực thiết kế NextLevelBuilder: design tokens, layout hierarchy và responsiveness. |
| **Design Direction** | [impeccable-design](../impeccable-design/SKILL.md) | Giám đốc thiết kế AI: các lệnh `craft`, `shape`, `polish`, `audit`, `bolder`, `typeset`, `delight`. |
| **Anti-Slop Web** | [taste-skill-web](../taste-skill-web/SKILL.md) / [taste-skill-v1](../taste-skill-v1/SKILL.md) | Chống template AI sáo rỗng, tạo typography rộng và bento grids phá cách. |
| **Brand Identity** | [brandkit](../brandkit/SKILL.md) | Tạo bảng hướng dẫn thương hiệu (brand-guidelines), bảng màu, typography và logo system. |
| **Mobile Polish** | [mobile-native](../mobile-native/SKILL.md) | Xử lý cảm ứng mượt mà trên điện thoại: chống tap lag, xử lý notch, thanh địa chỉ 100vh. |
| **Feedback & Toast** | [ask-sonner](../ask-sonner/SKILL.md) | Cài đặt và tích hợp Sonner toast notifications (promise toast, custom styling, dark mode). |
| **Motion & Physics** | [animate](../animate/SKILL.md), [animate-expo](../animate-expo/SKILL.md) | Xây dựng chuyển động web/mobile từ đầu với đường cong gia tốc và lò xo vật lý chuẩn. |
| **Apple Motion** | [apple-design](../apple-design/SKILL.md) | Trải nghiệm người dùng kiểu Apple: physics springs, translucent materials, dynamic depth. |
| **Micro-Interactions** | [emil-design-eng](../emil-design-eng/SKILL.md) | Triết lý Emil Kowalski về những chi tiết vi mô vô hình tạo cảm giác phần mềm cao cấp. |
| **Motion Discovery** | [find-animation-opportunities](../find-animation-opportunities/SKILL.md) | Rà soát giao diện và đề xuất các vị trí nên bổ sung micro-animation có chủ đích. |
| **Motion Audit** | [improve-animations](../improve-animations/SKILL.md), [review-animations](../review-animations/SKILL.md) | Đánh giá và khắc phục các animation bị giật, sai thời lượng hoặc sai easing. |
| **GSAP Advanced** | [gpt-tasteskill](../gpt-tasteskill/SKILL.md) | Hiệu ứng cuộn nâng cao GSAP ScrollTrigger, pinning, scrubbing và gapless bento grid. |
| **Chuyên Biệt Thẩm Mỹ** | [brutalist-skill](../brutalist-skill/SKILL.md), [minimalist-skill](../minimalist-skill/SKILL.md), [soft-skill](../soft-skill/SKILL.md), [stitch-skill](../stitch-skill/SKILL.md) | Chuyển đổi linh hoạt giữa Industrial Brutalist, Clean Minimalist, Luxury Agency, Google Stitch. |
| **Sinh Ảnh ➔ Code** | [image-to-code-skill](../image-to-code-skill/SKILL.md), [imagegen-frontend-web](../imagegen-frontend-web/SKILL.md), [imagegen-frontend-mobile](../imagegen-frontend-mobile/SKILL.md) | Tự động tạo ảnh mockup chất lượng cao trước, sau đó chuyển thành mã nguồn HTML/CSS chuẩn xác. |
| **Tooling & Output** | [pick-ui-library](../pick-ui-library/SKILL.md), [prototype](../prototype/SKILL.md), [output-skill](../output-skill/SKILL.md) | Chọn thư viện UI, tạo prototype nhanh, và bắt buộc sinh mã CSS/JS toàn vẹn 100%. |
