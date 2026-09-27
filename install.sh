#!/usr/bin/env bash
# ==============================================================================
# Universal DevCycle & Engineering Skills Installer
# ==============================================================================
# Hỗ trợ đa nền tảng: Ubuntu / Debian / Fedora / Arch / macOS / Windows (Git Bash, WSL, MSYS2)
#
# Quy trình cài đặt thông minh & nhanh chóng:
# 1. Tự động phát hiện hệ điều hành và thư mục Antigravity IDE (~/.gemini/config/skills).
# 2. Kiểm tra môi trường hệ thống (Python, Node.js, npm, graft, graphify, ruff...).
# 3. Duyệt danh sách toàn bộ kỹ năng (skills):
#    - Nếu skill ĐÃ CÓ ở Antigravity IDE: Bỏ qua (skip) để cài đặt siêu tốc.
#    - Nếu skill CHƯA CÓ ở Antigravity IDE:
#      + Nếu skill ĐÃ CÓ trong thư mục này: Thực hiện cài luôn từ thư mục nội bộ.
#      + Nếu skill CHƯA CÓ trong thư mục này: Tự động clone từ GitHub nguồn & cài đặt.
# ==============================================================================

set -euo pipefail

# ------------------------------------------------------------------------------
# Màu sắc hiển thị
# ------------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORCE=0
MODE="copy" # "copy" hoặc "link"
CUSTOM_TARGET=""
INSTALL_SECURITY_TOOLS=0

# ------------------------------------------------------------------------------
# Danh mục nguồn GitHub của các bộ Skill (Fallback khi local chưa có)
# ------------------------------------------------------------------------------
REPO_EMIL="https://github.com/emilkowalski/skills.git"
REPO_TASTE="https://github.com/Leonxlnx/taste-skill.git"
REPO_IMPECCABLE="https://github.com/pbakaus/impeccable.git"

# Danh mục 46 skills chuẩn
KNOWN_SKILLS=(
    # 1. DevCycle Lifecycle Suite & Core Senior Engineering
    "devcycle"
    "devcycle-audit"
    "devcycle-bugfix"
    "devcycle-debug"
    "devcycle-e2e"
    "devcycle-index"
    "devcycle-issues"
    "devcycle-refine"
    "devcycle-security"
    "devcycle-spec"
    "devcycle-tdd"
    "devcycle-ui"
    "jira-bugfix"
    "jira-fetch"
    "senior-dev-pipeline"
    "spec-engineering"
    "tdd-development"
    "redteam-security"
    "ui-ux-pro-max"

    # 2. Animation & Interaction (emilkowalski/skills)
    "animate"
    "animate-expo"
    "animation-vocabulary"
    "apple-design"
    "ask-sonner"
    "emil-design-eng"
    "find-animation-opportunities"
    "improve-animations"
    "mobile-native"
    "pick-ui-library"
    "prototype"
    "review-animations"
    "write-swift"

    # 3. Aesthetic & Taste Design (Leonxlnx/taste-skill)
    "brandkit"
    "brutalist-skill"
    "gpt-tasteskill"
    "image-to-code-skill"
    "imagegen-frontend-mobile"
    "imagegen-frontend-web"
    "minimalist-skill"
    "output-skill"
    "redesign-skill"
    "soft-skill"
    "stitch-skill"
    "taste-skill-v1"
    "taste-skill-web"

    # 4. Impeccable Design System (pbakaus/impeccable)
    "impeccable-design"
)

# ------------------------------------------------------------------------------
# Hàm thông báo / Logging
# ------------------------------------------------------------------------------
print_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "================================================================================"
    echo "    ⚡ UNIVERSAL DEVCYCLE & ENGINEERING SKILLS AUTO-INSTALLER ⚡"
    echo "       (Hỗ trợ tối ưu Windows Git Bash / WSL / Ubuntu / macOS)"
    echo "================================================================================"
    echo -e "${NC}"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_skip() {
    echo -e "  ${YELLOW}⊘ [ĐÃ CÓ]${NC} $1 (bỏ qua)"
}

log_installed_local() {
    echo -e "  ${GREEN}✓ [CÀI TỪ THƯ MỤC]${NC} $1"
}

log_installed_remote() {
    echo -e "  ${MAGENTA}⚡ [CLONE GITHUB & CÀI ĐẶT]${NC} $1"
}

# ------------------------------------------------------------------------------
# Tự động phát hiện hệ điều hành & Thư mục đích của Antigravity IDE
# ------------------------------------------------------------------------------
detect_default_target_dir() {
    if [[ -n "${CUSTOM_TARGET}" ]]; then
        echo "${CUSTOM_TARGET}"
        return
    fi

    local os_type
    os_type="$(uname -s 2>/dev/null || echo "Unknown")"

    case "${os_type}" in
        CYGWIN*|MINGW*|MSYS*)
            # Môi trường Windows (Git Bash, MSYS2, Cygwin)
            if [[ -n "${USERPROFILE:-}" ]]; then
                if command -v cygpath &>/dev/null; then
                    echo "$(cygpath -u "${USERPROFILE}")/.gemini/config/skills"
                else
                    echo "${USERPROFILE//\\//}/.gemini/config/skills"
                fi
            else
                echo "${HOME}/.gemini/config/skills"
            fi
            ;;
        Linux*)
            # Nếu trong WSL và người dùng có thư mục Windows User Profile
            # Mặc định vẫn dùng $HOME/.gemini/config/skills cho môi trường Linux/WSL
            echo "${HOME}/.gemini/config/skills"
            ;;
        Darwin*)
            # macOS
            echo "${HOME}/.gemini/config/skills"
            ;;
        *)
            echo "${HOME}/.gemini/config/skills"
            ;;
    esac
}

# ------------------------------------------------------------------------------
# Sao chép file đa nền tảng (Hoạt động cả khi không có rsync trên Windows)
# ------------------------------------------------------------------------------
copy_dir_cross_platform() {
    local src_dir="$1"
    local dst_dir="$2"

    mkdir -p "${dst_dir}"

    if command -v rsync &>/dev/null; then
        rsync -a --delete "${src_dir}/" "${dst_dir}/"
    else
        # Fallback cho môi trường Windows Git Bash không có rsync
        rm -rf "${dst_dir:?}"/* 2>/dev/null || true
        cp -R "${src_dir}/." "${dst_dir}/"
    fi
}

UPGRADE_ENV=0
AUTO_INSTALL_ENV=1

# ------------------------------------------------------------------------------
# Xử lý tham số dòng lệnh
# ------------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --target)
            CUSTOM_TARGET="$2"
            shift 2
            ;;
        --force|-f)
            FORCE=1
            shift
            ;;
        --upgrade-env)
            UPGRADE_ENV=1
            shift
            ;;
        --no-env-install)
            AUTO_INSTALL_ENV=0
            shift
            ;;
        --link)
            MODE="link"
            shift
            ;;
        --security-tools)
            INSTALL_SECURITY_TOOLS=1
            shift
            ;;
        --help|-h)
            echo "Cách dùng: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --target <DIR>       Chỉ định thư mục đích (mặc định: ~/.gemini/config/skills hoặc %USERPROFILE%/.gemini/config/skills)"
            echo "  --force, -f          Cài đặt lại toàn bộ (ghi đè ngay cả khi skill đã có)"
            echo "  --upgrade-env        Tự động nâng cấp Python & Node.js lên bản mới nhất ngay cả khi đã có"
            echo "  --no-env-install     Bỏ qua bước tự động cài đặt Python/Node.js"
            echo "  --security-tools     Tự động cài đặt bộ công cụ an ninh mã nguồn & API (semgrep, bandit, pip-audit, detect-secrets, schemathesis, checkov)"
            echo "  --link               Tạo symlink thay vì copy file (khuyến nghị trên Linux/macOS)"
            echo "  --help, -h           Hiển thị hướng dẫn này"
            exit 0
            ;;
        *)
            log_error "Tham số không hợp lệ: $1"
            echo "Dùng $0 --help để xem hướng dẫn."
            exit 1
            ;;
    esac
done

TARGET_DIR="$(detect_default_target_dir)"

print_banner

OS_INFO="$(uname -s 2>/dev/null || echo "Unknown")"
echo -e "Hệ điều hành  : ${BOLD}${OS_INFO}${NC}"
echo -e "Thư mục nguồn : ${BOLD}${SCRIPT_DIR}${NC}"
echo -e "Thư mục đích  : ${CYAN}${BOLD}${TARGET_DIR}${NC}"
echo -e "Chế độ cài đặt: ${BOLD}${MODE}${NC} (Force: $([[ ${FORCE} -eq 1 ]] && echo -e "${YELLOW}BẬT${NC}" || echo -e "${GREEN}TẮT${NC}"))\n"

# ------------------------------------------------------------------------------
# 1. Kiểm tra & Tự động cài đặt Môi trường (Python & Node.js mới nhất)
# ------------------------------------------------------------------------------
log_info "1. Đang kiểm tra & chuẩn bị môi trường Runtime (Python & Node.js mới nhất)..."

# Đảm bảo các thư mục binary người dùng nằm trong PATH
for bin_path in "$HOME/.local/bin" "$HOME/.cargo/bin" "$HOME/.fnm" "${USERPROFILE:-}/.cargo/bin"; do
    if [[ -d "${bin_path}" && ":$PATH:" != *":${bin_path}:"* ]]; then
        export PATH="${bin_path}:$PATH"
    fi
done

# ------------------------------------------------------------------------------
# 1.1 Tự động cài đặt / Nâng cấp Python phiên bản mới nhất
# ------------------------------------------------------------------------------
detect_python() {
    PYTHON_CMD=""
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &>/dev/null; then
        PYTHON_CMD="python"
    elif command -v py &>/dev/null; then
        PYTHON_CMD="py"
    fi
}

detect_python
PY_NEED_INSTALL=0

if [[ -z "${PYTHON_CMD}" ]]; then
    PY_NEED_INSTALL=1
else
    PY_MAJOR="$(${PYTHON_CMD} -c "import sys; print(sys.version_info.major)" 2>/dev/null || echo 0)"
    PY_MINOR="$(${PYTHON_CMD} -c "import sys; print(sys.version_info.minor)" 2>/dev/null || echo 0)"
    if [[ ${PY_MAJOR} -lt 3 || ${PY_MINOR} -lt 10 || ${UPGRADE_ENV} -eq 1 ]]; then
        PY_NEED_INSTALL=1
    fi
fi

if [[ ${PY_NEED_INSTALL} -eq 1 && ${AUTO_INSTALL_ENV} -eq 1 ]]; then
    log_info "Đang tự động cài đặt / nâng cấp Python phiên bản mới nhất..."
    case "${OS_INFO}" in
        Linux*)
            # Nếu có sudo: cài các gói hệ thống cần thiết
            if command -v apt-get &>/dev/null && command -v sudo &>/dev/null && (sudo -n true 2>/dev/null || sudo -v 2>/dev/null); then
                log_info "  Đang cài đặt python3, pip, venv qua apt..."
                sudo apt-get update -qq || true
                sudo apt-get install -y -qq python3 python3-pip python3-venv python3-setuptools || true
            fi

            # Cài đặt uv (Astral) để quản lý phiên bản Python mới nhất
            if ! command -v uv &>/dev/null; then
                log_info "  Đang tải công cụ quản lý Python uv..."
                curl -LsSf https://astral.sh/uv/install.sh | sh 2>/dev/null || true
                export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
            fi

            if command -v uv &>/dev/null; then
                log_info "  Đang cài đặt Python mới nhất thông qua uv..."
                uv python install latest || true
            fi
            ;;
        CYGWIN*|MINGW*|MSYS*)
            # Windows
            if command -v winget &>/dev/null || command -v winget.exe &>/dev/null; then
                log_info "  Đang cài đặt Python mới nhất qua winget..."
                (winget install Python.Python.3.12 -e --silent --accept-source-agreements --accept-package-agreements || winget install Python.Python.3 -e --silent --accept-source-agreements --accept-package-agreements) || true
            elif command -v choco &>/dev/null; then
                log_info "  Đang cài đặt Python qua Chocolatey..."
                choco install python -y || true
            elif command -v scoop &>/dev/null; then
                log_info "  Đang cài đặt Python qua Scoop..."
                scoop install python || true
            fi
            # uv fallback cho Windows
            if ! command -v uv &>/dev/null; then
                curl -LsSf https://astral.sh/uv/install.sh | sh 2>/dev/null || true
                export PATH="$HOME/.local/bin:$USERPROFILE/.cargo/bin:$PATH"
            fi
            if command -v uv &>/dev/null; then
                uv python install latest 2>/dev/null || true
            fi
            ;;
        Darwin*)
            if command -v brew &>/dev/null; then
                brew install python || brew upgrade python || true
            fi
            ;;
    esac
fi

# Nhận diện lại Python sau cài đặt
detect_python
if [[ -n "${PYTHON_CMD}" ]]; then
    PY_VER=$(${PYTHON_CMD} --version 2>&1)
    log_success "Python: ${PY_VER} (${PYTHON_CMD})"
else
    log_warning "Chưa thể cài đặt tự động Python. Vui lòng cài thủ công từ https://python.org/"
fi

# ------------------------------------------------------------------------------
# 1.2 Tự động cài đặt / Nâng cấp Node.js phiên bản mới nhất
# ------------------------------------------------------------------------------
NODE_CUR_VER=""
NODE_MAJOR=0
if command -v node &>/dev/null; then
    NODE_CUR_VER="$(node -v 2>/dev/null || echo "")"
    NODE_MAJOR="$(echo "${NODE_CUR_VER}" | sed -E 's/^v([0-9]+).*/\1/' || echo 0)"
fi

NODE_NEED_INSTALL=0
if [[ -z "${NODE_CUR_VER}" || ${NODE_MAJOR} -lt 20 || ${UPGRADE_ENV} -eq 1 ]]; then
    NODE_NEED_INSTALL=1
fi

if [[ ${NODE_NEED_INSTALL} -eq 1 && ${AUTO_INSTALL_ENV} -eq 1 ]]; then
    log_info "Đang tự động cài đặt / nâng cấp Node.js lên phiên bản mới nhất (LTS/Current)..."
    case "${OS_INFO}" in
        Linux*)
            # Nếu có sudo: dùng kho chính thức NodeSource (LTS 22.x hoặc current)
            if command -v apt-get &>/dev/null && command -v sudo &>/dev/null && (sudo -n true 2>/dev/null || sudo -v 2>/dev/null); then
                log_info "  Đang cấu hình kho lưu trữ chính thức NodeSource (Node.js 22.x LTS)..."
                curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - || true
                sudo apt-get install -y -qq nodejs || true
            elif command -v dnf &>/dev/null && command -v sudo &>/dev/null && (sudo -n true 2>/dev/null || sudo -v 2>/dev/null); then
                sudo dnf install -y -q nodejs npm || true
            elif command -v pacman &>/dev/null && command -v sudo &>/dev/null && (sudo -n true 2>/dev/null || sudo -v 2>/dev/null); then
                sudo pacman -S --noconfirm nodejs npm || true
            else
                # Fallback không cần root: fnm (Fast Node Manager)
                log_info "  Đang cài đặt Node.js mới nhất qua fnm (User-space)..."
                curl -fsSL https://fnm.vercel.app/install | bash -s -- --install-dir "$HOME/.local/bin" --skip-shell 2>/dev/null || true
                export PATH="$HOME/.local/bin:$PATH"
                if command -v fnm &>/dev/null; then
                    eval "$(fnm env 2>/dev/null || true)"
                    fnm install --lts || fnm install latest || true
                    fnm default lts-latest 2>/dev/null || true
                fi
            fi
            ;;
        CYGWIN*|MINGW*|MSYS*)
            # Windows
            if command -v winget &>/dev/null || command -v winget.exe &>/dev/null; then
                log_info "  Đang cài đặt Node.js mới nhất qua winget..."
                (winget install OpenJS.NodeJS.LTS -e --silent --accept-source-agreements --accept-package-agreements || winget install OpenJS.NodeJS -e --silent --accept-source-agreements --accept-package-agreements) || true
            elif command -v choco &>/dev/null; then
                log_info "  Đang cài đặt Node.js qua Chocolatey..."
                choco install nodejs-lts -y || choco install nodejs -y || true
            elif command -v scoop &>/dev/null; then
                log_info "  Đang cài đặt Node.js qua Scoop..."
                scoop install nodejs-lts || scoop install nodejs || true
            else
                # Cài đặt qua fnm cho Windows
                log_info "  Đang cài đặt Node.js qua fnm..."
                curl -fsSL https://fnm.vercel.app/install | bash 2>/dev/null || true
                export PATH="$HOME/.local/bin:$USERPROFILE/.fnm:$PATH"
                if command -v fnm &>/dev/null; then
                    eval "$(fnm env 2>/dev/null || true)"
                    fnm install --lts || true
                fi
            fi
            ;;
        Darwin*)
            if command -v brew &>/dev/null; then
                brew install node || brew upgrade node || true
            fi
            ;;
    esac
fi

# Kiểm tra lại Node.js & npm sau cài đặt
if command -v node &>/dev/null && command -v npm &>/dev/null; then
    NODE_VER=$(node --version)
    NPM_VER=$(npm --version)
    log_success "Node.js: ${NODE_VER} | npm: ${NPM_VER}"
else
    log_warning "Node.js hoặc npm chưa được cài đặt hoàn tất. Graft cần Node.js để chạy."
fi

# ------------------------------------------------------------------------------
# 1.3 Kiểm tra Git
# ------------------------------------------------------------------------------
if command -v git &>/dev/null; then
    log_success "Git: Đã sẵn sàng ($(git --version))"
else
    log_info "Đang cài đặt Git..."
    if command -v apt-get &>/dev/null && command -v sudo &>/dev/null && (sudo -n true 2>/dev/null || sudo -v 2>/dev/null); then
        sudo apt-get install -y -qq git || true
    elif command -v winget &>/dev/null || command -v winget.exe &>/dev/null; then
        winget install Git.Git -e --silent --accept-source-agreements --accept-package-agreements || true
    fi
    if command -v git &>/dev/null; then
        log_success "Git: Cài đặt thành công!"
    else
        log_warning "Không tìm thấy git. Tính năng clone skill từ GitHub có thể không khả dụng nếu thiếu local skill."
    fi
fi

# ------------------------------------------------------------------------------
# 2. Cài đặt các công cụ Dual-Engine & Linter (Graft, Graphify, Ruff)
# ------------------------------------------------------------------------------
log_info "2. Đang kiểm tra các công cụ CLI cần thiết..."

# 2.1 Graft (@nanonets/graft)
if command -v graft &>/dev/null; then
    log_success "Graft: Đã cài đặt ($(graft --version 2>/dev/null || echo 'OK'))"
else
    if command -v npm &>/dev/null; then
        log_info "Đang cài đặt Graft (@nanonets/graft)..."
        npm install -g @nanonets/graft || npm install --prefix "$HOME/.local" -g @nanonets/graft || log_warning "Không thể cài đặt tự động graft qua npm."
        if command -v graft &>/dev/null; then
            log_success "Graft: Cài đặt thành công!"
        fi
    else
        log_warning "Chưa có npm để cài graft."
    fi
fi

# 2.2 Graphify (graphifyy)
if command -v graphify &>/dev/null; then
    log_success "Graphify: Đã cài đặt ($(graphify --version 2>/dev/null || echo 'OK'))"
else
    if [[ -n "${PYTHON_CMD}" ]]; then
        log_info "Đang kiểm tra cài đặt Graphify (graphifyy)..."
        if command -v uv &>/dev/null; then
            uv tool install graphifyy || true
        elif command -v pipx &>/dev/null; then
            pipx install graphifyy || true
        elif ${PYTHON_CMD} -m pip --version &>/dev/null; then
            ${PYTHON_CMD} -m pip install --user graphifyy || ${PYTHON_CMD} -m pip install --break-system-packages --user graphifyy || true
        fi
        if command -v graphify &>/dev/null; then
            log_success "Graphify: Cài đặt thành công!"
        fi
    fi
fi

# 2.3 Ruff (Linter siêu tốc)
if command -v ruff &>/dev/null; then
    log_success "Ruff: Đã cài đặt ($(ruff --version 2>/dev/null || echo 'OK'))"
else
    if command -v uv &>/dev/null; then
        uv tool install ruff || true
    elif command -v pipx &>/dev/null; then
        pipx install ruff || true
    fi
fi

# 2.4 Bộ công cụ An ninh mạng & Pentesting (devcycle-security)
if [[ ${INSTALL_SECURITY_TOOLS} -eq 1 ]]; then
    log_info "Đang chuẩn bị và cài đặt bộ công cụ an ninh nòng cốt (SAST, SCA, Secrets, API)..."
    if [[ -n "${PYTHON_CMD}" ]]; then
        SEC_PACKAGES=("semgrep" "bandit" "pip-audit" "detect-secrets" "schemathesis" "checkov")
        for pkg in "${SEC_PACKAGES[@]}"; do
            if command -v "$pkg" &>/dev/null; then
                log_success "Bảo mật: $pkg đã sẵn sàng."
            else
                log_info "Đang cài đặt $pkg..."
                if command -v uv &>/dev/null; then
                    uv tool install "$pkg" || true
                elif command -v pipx &>/dev/null; then
                    pipx install "$pkg" || true
                else
                    ${PYTHON_CMD} -m pip install --user "$pkg" || ${PYTHON_CMD} -m pip install --break-system-packages --user "$pkg" || log_warning "Không thể cài đặt tự động $pkg."
                fi
            fi
        done
    fi
fi

# ------------------------------------------------------------------------------
# 3. Thu thập toàn bộ danh sách Skills cần triển khai
# ------------------------------------------------------------------------------
log_info "3. Đang thu thập và kiểm tra danh sách Skills..."

# Tập hợp danh sách kỹ năng duy nhất: kết hợp thư mục hiện tại + catalog chuẩn
declare -A ALL_SKILLS_MAP=()

# 1. Quét mọi thư mục trong SCRIPT_DIR có file SKILL.md
while IFS= read -r skill_dir; do
    skill_name="$(basename "${skill_dir}")"
    if [[ -n "${skill_name}" && "${skill_name}" != "." && "${skill_name}" != ".." ]]; then
        ALL_SKILLS_MAP["${skill_name}"]=1
    fi
done < <(find "${SCRIPT_DIR}" -maxdepth 2 -mindepth 2 -name "SKILL.md" -exec dirname {} \;)

# 2. Bổ sung các skill trong catalog đã biết
for s in "${KNOWN_SKILLS[@]}"; do
    ALL_SKILLS_MAP["${s}"]=1
done

# Chuyển thành danh sách mảng và sắp xếp theo bảng chữ cái
IFS=$'\n' SORTED_SKILLS=($(sort <<<"${!ALL_SKILLS_MAP[*]}"))
unset IFS

TOTAL_SKILLS="${#SORTED_SKILLS[@]}"
log_info "Tổng số skill trong hệ thống cần quản lý: ${BOLD}${TOTAL_SKILLS}${NC}"

mkdir -p "${TARGET_DIR}"

# Dọn dẹp symlink hỏng hoặc thư mục monorepo cũ nếu có
find "${TARGET_DIR}" -maxdepth 1 -type l -exec rm -f {} + 2>/dev/null || true
rm -rf "${TARGET_DIR}/emilkowalski-skills" "${TARGET_DIR}/taste-skill" "${TARGET_DIR}/impeccable" 2>/dev/null || true

# ------------------------------------------------------------------------------
# Hàm clone từ GitHub khi local chưa có
# ------------------------------------------------------------------------------
TEMP_CLONE_DIR=""
cleanup_temp() {
    if [[ -n "${TEMP_CLONE_DIR}" && -d "${TEMP_CLONE_DIR}" ]]; then
        rm -rf "${TEMP_CLONE_DIR}" 2>/dev/null || true
    fi
}
trap cleanup_temp EXIT

clone_and_install_remote_skill() {
    local skill="$1"
    local repo_url=""
    local sub_path=""

    case "${skill}" in
        # Emil Kowalski skills
        animate|animate-expo|animation-vocabulary|apple-design|ask-sonner|emil-design-eng|\
        find-animation-opportunities|improve-animations|mobile-native|pick-ui-library|\
        prototype|review-animations|write-swift)
            repo_url="${REPO_EMIL}"
            sub_path="skills/${skill}"
            ;;
        # Taste skills
        taste-skill-web)
            repo_url="${REPO_TASTE}"
            sub_path="skills/taste-skill"
            ;;
        brandkit|brutalist-skill|gpt-tasteskill|image-to-code-skill|imagegen-frontend-mobile|\
        imagegen-frontend-web|minimalist-skill|output-skill|redesign-skill|soft-skill|\
        stitch-skill|taste-skill-v1)
            repo_url="${REPO_TASTE}"
            sub_path="skills/${skill}"
            ;;
        # Impeccable skill
        impeccable-design)
            repo_url="${REPO_IMPECCABLE}"
            sub_path="plugin/skills/impeccable"
            ;;
        *)
            repo_url=""
            ;;
    esac

    if [[ -z "${repo_url}" ]]; then
        log_error "Không xác định được GitHub repo cho skill '${skill}' và không có sẵn trong thư mục."
        return 1
    fi

    if ! command -v git &>/dev/null; then
        log_error "Cần có git để clone skill '${skill}' từ GitHub: ${repo_url}"
        return 1
    fi

    if [[ -z "${TEMP_CLONE_DIR}" ]]; then
        TEMP_CLONE_DIR="$(mktemp -d 2>/dev/null || mktemp -d -t 'dev_skills_clone_XXXXXX')"
    fi

    local repo_name
    repo_name="$(basename "${repo_url}" .git)"
    local cached_repo="${TEMP_CLONE_DIR}/${repo_name}"

    if [[ ! -d "${cached_repo}" ]]; then
        log_info "  Đang clone nhanh (--depth 1) ${repo_name} từ GitHub..."
        git clone --depth 1 -q "${repo_url}" "${cached_repo}" || {
            log_error "Clone ${repo_url} thất bại."
            return 1
        }
    fi

    local extracted_src="${cached_repo}/${sub_path}"
    if [[ ! -f "${extracted_src}/SKILL.md" ]]; then
        log_error "Không tìm thấy SKILL.md tại ${sub_path} trong repo ${repo_name}."
        return 1
    fi

    # Lưu lại vào SCRIPT_DIR để lần sau có sẵn luôn (nhanh chóng)
    copy_dir_cross_platform "${extracted_src}" "${SCRIPT_DIR}/${skill}"

    # Cài đặt vào TARGET_DIR
    if [[ "${MODE}" == "link" ]]; then
        ln -sfn "${SCRIPT_DIR}/${skill}" "${TARGET_DIR}/${skill}"
    else
        copy_dir_cross_platform "${extracted_src}" "${TARGET_DIR}/${skill}"
    fi

    log_installed_remote "${skill}"
    return 0
}

# ------------------------------------------------------------------------------
# 4. Thực hiện cài đặt theo đúng logic yêu cầu
# ------------------------------------------------------------------------------
log_info "4. Đang tiến hành kiểm tra & triển khai từng Skill..."

SKIPPED_COUNT=0
LOCAL_COUNT=0
REMOTE_COUNT=0
ERROR_COUNT=0

for skill in "${SORTED_SKILLS[@]}"; do
    target_skill_path="${TARGET_DIR}/${skill}"
    local_skill_path="${SCRIPT_DIR}/${skill}"

    # Kiểm tra xem Antigravity IDE đã có skill này hay chưa
    if [[ -f "${target_skill_path}/SKILL.md" && ${FORCE} -eq 0 ]]; then
        log_skip "${skill}"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        continue
    fi

    # Nếu chưa có ở Antigravity IDE (hoặc người dùng chỉ định --force):
    if [[ -f "${local_skill_path}/SKILL.md" ]]; then
        # Đã có trong thư mục hiện tại -> Thực hiện cài luôn!
        if [[ "${MODE}" == "link" ]]; then
            ln -sfn "${local_skill_path}" "${target_skill_path}"
        else
            copy_dir_cross_platform "${local_skill_path}" "${target_skill_path}"
        fi
        log_installed_local "${skill}"
        LOCAL_COUNT=$((LOCAL_COUNT + 1))
    else
        # Chưa có trong thư mục này -> Clone từ GitHub và cài đặt!
        if clone_and_install_remote_skill "${skill}"; then
            REMOTE_COUNT=$((REMOTE_COUNT + 1))
        else
            ERROR_COUNT=$((ERROR_COUNT + 1))
        fi
    fi
done

# Đồng bộ file CLAUDE.md và README.md nếu cần
if [[ -f "${SCRIPT_DIR}/CLAUDE.md" ]]; then
    cp -f "${SCRIPT_DIR}/CLAUDE.md" "${TARGET_DIR}/" 2>/dev/null || true
fi
if [[ -f "${SCRIPT_DIR}/README.md" ]]; then
    cp -f "${SCRIPT_DIR}/README.md" "${TARGET_DIR}/" 2>/dev/null || true
fi

# Cấp quyền thực thi cho các file script
find "${TARGET_DIR}" -type f \( -name "*.py" -o -name "*.sh" \) -exec chmod +x {} + 2>/dev/null || true

# ------------------------------------------------------------------------------
# 5. Tổng kết kết quả cài đặt
# ------------------------------------------------------------------------------
TOTAL_AVAILABLE=$(find "${TARGET_DIR}" -maxdepth 2 -name "SKILL.md" 2>/dev/null | wc -l)

echo ""
echo -e "${GREEN}${BOLD}================================================================================${NC}"
echo -e "${GREEN}${BOLD}                 🎉 CÀI ĐẶT HOÀN TẤT THÀNH CÔNG! 🎉${NC}"
echo -e "${GREEN}${BOLD}================================================================================${NC}"
echo -e "Thư mục cài đặt Antigravity: ${CYAN}${BOLD}${TARGET_DIR}${NC}"
echo -e "Tổng số skill sẵn sàng     : ${BOLD}${TOTAL_AVAILABLE} skills${NC}"
echo -e "  • Đã có sẵn (giữ nguyên) : ${YELLOW}${SKIPPED_COUNT}${NC}"
echo -e "  • Cài đặt từ thư mục     : ${GREEN}${LOCAL_COUNT}${NC}"
echo -e "  • Clone GitHub & cài đặt : ${MAGENTA}${REMOTE_COUNT}${NC}"
if [[ ${ERROR_COUNT} -gt 0 ]]; then
    echo -e "  • Lỗi cần kiểm tra       : ${RED}${ERROR_COUNT}${NC}"
fi
echo ""
echo -e "${BOLD}Các lệnh nhanh sẵn sàng sử dụng trong Antigravity:${NC}"
echo -e "  • ${CYAN}/devcycle \"tên tính năng\"${NC}      : Chạy trọn vẹn quy trình DevCycle từ A-Z"
echo -e "  • ${CYAN}/devcycle-spec \"mô tả\"${NC}          : Sinh PRD & Acceptance Criteria chống ảo giác"
echo -e "  • ${CYAN}/devcycle-tdd \"tên task\"${NC}         : Lập trình TDD chuẩn Matt Pocock"
echo -e "  • ${CYAN}/devcycle-security .${NC}             : Đánh giá an ninh Red-Team & SAST/DAST"
echo -e "  • ${CYAN}/devcycle-ui \"mô tả\"${NC}              : Thiết kế giao diện UI/UX Pro Max"
echo ""
