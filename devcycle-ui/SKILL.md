---
name: devcycle-ui
description: "UI/UX builder & design intelligence based on NextLevelBuilder UI-UX Pro Max standards + Anthropic frontend-design + taste-skill (anti-slop) + impeccable (award-winning design director) + emilkowalski/skills (motion & animation). Supports Web (Tailwind, Vanilla CSS, React, Vue, Next.js) and Desktop (PySide6, Qt, QML, QSS). Triggers: \"design UI\", \"build UI\", \"style this window\", \"create component\", \"devcycle-ui\", \"frontend-design\", \"thiết kế giao diện\", \"animate\", \"motion\", \"polish design\", \"impeccable\"."
argument-hint: "What screen, component, or theme to design?"
---

# Devcycle — UI (Universal UI/UX Builder & Design Intelligence)

Provides world-class design systems, component patterns, and visual styling for both
**Web applications** (Tailwind CSS, Vanilla CSS, React, Next.js) and **Desktop apps** (PySide6, Qt, QML, QSS).

Powered by **4 elite external skill packs** installed at system level:

| Pack | Description | Skills available |
|------|-------------|-----------------|
| **frontend-design** (Anthropic) | Distinctive, opinionated visual design & anti-template lead | `frontend-design` |
| **taste-skill** (Leonxlnx) | Anti-slop frontend framework | `taste-skill-web`, `brutalist-skill`, `minimalist-skill`, `soft-skill`, `redesign-skill`, `output-skill`, `stitch-skill` |
| **impeccable** (pbakaus) | Award-winning design director AI | `impeccable-design` with commands: craft, shape, audit, polish, bolder, animate, colorize, typeset, layout, delight |
| **emilkowalski/skills** | Motion & animation engineering | `animate`, `review-animations`, `improve-animations`, `find-animation-opportunities`, `animation-performance`, `break-ui`, `animation-vocabulary`, `apple-design`, `pick-ui-library` |

---

## 0. BRIEF INFERENCE & SUBJECT GROUNDING (Read the Room First)

Before touching any code, act as the design lead: **ground your design in the subject matter** (its industry, materials, vernacular) and infer what the user actually wants. State a clear "Design Read":

> **"Reading this as: `<subject & page kind>` for `<target audience>`, solving `<primary job>`, with a `<vibe>` language, leaning toward `<design system or aesthetic family>`."**

### Anti-Default Discipline (Purging AI Tells — from Anthropic & taste-skill)
NEVER fall into the 5 classic tells of AI-generated design:
1. **Cream + Terracotta serif**: Warm cream background (~`#F4F1EA`) with high-contrast serif display and clay/terracotta accent (~`#D97757`).
2. **Acid-on-dark**: Near-black background with a single bright acid-green or vermilion accent.
3. **Broadsheet newspaper**: Hairline rules, zero border-radius, dense multi-column newspaper styling.
4. **SaaS-card kit**: Content chopped into identical rounded cards, uniform border-radius, soft grey shadows (`rgba(0,0,0,.1)`), gradient washes as decoration.
5. **Template chrome & false sequencing**: Tracked-out ALL-CAPS eyebrows, middle dots (`A · B · C`), spaced em dash (`WORD — fragment`), `→` appended to buttons, single-word highlights in headings, or arbitrary `01 / 02 / 03` numbered markers when content is not a sequence.

---

## 1. Two-Pass Design & Critique Workflow (from Anthropic frontend-design)

### Pass 1: Plan & Ground
Brainstorm a compact design plan grounded in the subject before coding:
- **Palette**: Define 4–6 named hex values tailored to the subject.
- **Typography**: 1 or 2 distinct font families following *The Elements of Typographic Style*. Keep line lengths < 80 characters.
- **Layout**: Clear prose concept + ASCII wireframe with intentional alignment (left, center, or justified).
- **Principles**: What makes this specific experience memorable and unique.

### Pass 2: Self-Critique & Purge
Review the plan against the brief before writing code:
- Did any generic AI default slip in? If so, revise it and state why.
- **"Spend your boldness in one place"**: Let one element (hero, typography, interactive moment) be memorable; keep everything else quiet and disciplined. (Chanel rule: remove one accessory).
- **CSS Specificity**: Ensure clean hierarchy; prevent conflicting classes (e.g. `.section` vs `.cta` padding/margins).
- **Writing in Design**: Words are design content, not decoration. Use active voice ("Save changes", not "Submit"), match CTA verbs with toasts ("Publish" ➔ "Published"), no apologetic error messages, and treat empty states as invitations to act.

---

## 2. Core Design Aesthetics (Zero-Mediocrity Policy)

1. **Color & Elevation**:
   - Avoid generic base colors (pure red, green, blue). Use curated HSL tokens, sleek dark modes, and subtle gradients.
   - Use Glassmorphism (`backdrop-filter: blur()`) and soft layered drop-shadows where appropriate.
2. **Typography & Hierarchy**:
   - Modern typography (Inter, Plus Jakarta Sans, Outfit, Roboto, custom serifs for editorial).
   - Clear modular scale hierarchy (H1, H2, Body, Small) with intentional leading and tracking.
3. **Dynamic Motion & Micro-Animations**:
   - Apply Emil Kowalski & Anthropic motion philosophy: animate only what earns it, sparing, right curve, right duration.
   - Smooth hover states, active transitions, staggered reveals, spatial consistency.

---

## 3. The Three Dials (from taste-skill)

After the design read, set three dials that gate every layout, motion, and density decision:

- **`DESIGN_VARIANCE: 1-10`** → 1 = Perfect Symmetry, 10 = Artsy Chaos
- **`MOTION_INTENSITY: 1-10`** → 1 = Static, 10 = Cinematic / Physics
- **`VISUAL_DENSITY: 1-10`** → 1 = Art Gallery / Airy, 10 = Cockpit / Packed Data

---

## 4. Design Mode Selection (from impeccable)

Choose the correct mode based on the surface type:

- **Persuade** — Landing pages, marketing, campaigns. Earn attention and action.
- **Operate** — App UI, dashboards, editors, admin. Scanability & consistency over expression.
- **Read** — Docs, articles, guides. Structure for comprehension.
- **Experience** — Portfolios, galleries, showcases. The artifact leads.

---

## 5. Animation Rules (from emilkowalski/skills & Anthropic restraint)

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
3. Non-user-triggered motion used sparingly (one orchestrated hero moment beats scattered entrance animations on every card).
4. Reduced motion gating ships **with** the animation, not as follow-up.
5. Cheapest tool that works. Don't install a library for a fade.

---

## 6. Design Intelligence Knowledge Search (BM25 CLI)

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

## 7. Skill Delegation Guide

### For distinctive, opinionated aesthetic direction & anti-template UI
→ Activate `frontend-design` skill (Anthropic design lead framework)

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

## 8. Web & Desktop Workflows

### Web Applications (React / Vue / HTML + CSS)
- Execute Pass 1 (Plan & Ground) and Pass 2 (Self-Critique & Purge) before coding.
- Define CSS custom properties / Tailwind theme tokens (`--primary`, `--surface`, `--accent`).
- Separate UI view components from state / data-fetching logic.
- Apply taste-skill anti-slop discipline and Anthropic anti-default checks before shipping.
- Run impeccable `audit` + `polish` before final delivery.
- Verify with browser testing and screenshot captures.

### Desktop Applications (PySide6 / Qt)
- Generate `<Screen>.qml` + `<Screen>.qss` token-driven styles.
- Preview and capture headless screenshot:
  ```bash
  python ~/.gemini/config/skills/devcycle-ui/scripts/render_ui.py --qss ui/style.qss --screenshot preview.png
  ```

---

## 9. Quality Gates (before shipping any UI)

1. ✅ Subject matter grounded & Design Read declared (Brief Inference)
2. ✅ Two-pass plan & self-critique performed ("spend boldness in one place")
3. ✅ No LLM-default aesthetics (purged 5 AI tells & anti-slop check)
4. ✅ Typography deliberate (< 80 chars line length, no single-word highlights, sentence case)
5. ✅ Copywriting checked (active voice, matching CTA/toast verbs, user-centric)
6. ✅ Motion passes Emil Kowalski & Anthropic restraint rules (sparing, user-triggered)
7. ✅ Impeccable craft floor respected (no a11y violations, responsive, keyboard focus)
8. ✅ Screenshot captured for visual verification

---

## 10. Liên Kết Toàn Diện Hệ Sinh Thái UI/UX (Comprehensive UI Skill Ecosystem)

| Nhóm Năng Lực | Kỹ Năng Tích Hợp | Vai Trò & Trường Hợp Kích Hoạt |
|---|---|---|
| **Distinctive Aesthetics** | [frontend-design](../frontend-design/SKILL.md) | Định hướng thẩm mỹ khác biệt của Anthropic: loại bỏ khuôn mẫu AI, kiểu chữ có chủ đích, quy trình 2 bước Plan-Critique và copywriting chuẩn mực. |
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
| **Motion Performance** | [animation-performance](../animation-performance/SKILL.md) | Tối ưu hóa hiệu năng animation: frame budget 60/120fps, composite-only layers, và triệt tiêu drop frames. |
| **UI Stress Test** | [break-ui](../break-ui/SKILL.md) | Phá vỡ UI bằng dữ liệu khắc nghiệt (tên cực dài, email bất quy tắc, số lượng 0/1/1000) với toggle Demo/Worst-case. |
| **GSAP Advanced** | [gpt-tasteskill](../gpt-tasteskill/SKILL.md) | Hiệu ứng cuộn nâng cao GSAP ScrollTrigger, pinning, scrubbing và gapless bento grid. |
| **Chuyên Biệt Thẩm Mỹ** | [brutalist-skill](../brutalist-skill/SKILL.md), [minimalist-skill](../minimalist-skill/SKILL.md), [soft-skill](../soft-skill/SKILL.md), [stitch-skill](../stitch-skill/SKILL.md) | Chuyển đổi linh hoạt giữa Industrial Brutalist, Clean Minimalist, Luxury Agency, Google Stitch. |
| **Sinh Ảnh ➔ Code** | [image-to-code-skill](../image-to-code-skill/SKILL.md), [imagegen-frontend-web](../imagegen-frontend-web/SKILL.md), [imagegen-frontend-mobile](../imagegen-frontend-mobile/SKILL.md) | Tự động tạo ảnh mockup chất lượng cao trước, sau đó chuyển thành mã nguồn HTML/CSS chuẩn xác. |
| **Tooling & Output** | [pick-ui-library](../pick-ui-library/SKILL.md), [prototype](../prototype/SKILL.md), [output-skill](../output-skill/SKILL.md) | Chọn thư viện UI, tạo prototype nhanh, và bắt buộc sinh mã CSS/JS toàn vẹn 100%. |
