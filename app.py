import streamlit as st
import streamlit.components.v1 as components
from backend import AI, COLS, HUMAN, ROWS, ConnectFourGame

st.set_page_config(page_title="Four in a Row", layout="centered")

if "game" not in st.session_state:
    st.session_state.game = ConnectFourGame()

game = st.session_state.game

st.markdown(
    """
    <style>
    #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
    }
    .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
    }
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 600px;
    }

    .title-text {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 2.8rem;
        font-weight: 900;
        text-align: center;
        letter-spacing: -0.5px;
        text-transform: uppercase;
        color: #ffffff;
        margin-bottom: 14px;
    }

    .legend-box {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 44px;
        background-color: #161b22;
        border: 2px solid #30363d;
        border-radius: 8px;
        padding: 12px 20px;
        margin-bottom: 18px;
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: 0.4px;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .disc-icon {
        width: 22px;
        height: 22px;
        border-radius: 50%;
        display: inline-block;
    }
    .disc-red {
        background-color: #e63946;
        border: 2px solid #a8202c;
    }
    .disc-yellow {
        background-color: #ffb703;
        border: 2px solid #b88200;
    }

    .result-box {
        text-align: center;
        font-size: 1.6rem;
        font-weight: 900;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 16px;
        background-color: #1f2937;
        border: 2px solid #4b5563;
        color: #ffffff;
        text-transform: uppercase;
    }

    div.stButton > button {
        height: 48px;
        background-color: #161b22;
        color: #ffffff;
        border: 2px solid #30363d;
        border-radius: 8px;
        transition: none;
    }
    div.stButton > button:hover:not(:disabled) {
        background-color: #21262d;
        border-color: #8b949e;
        color: #ffffff;
    }
    div.stButton > button:disabled {
        opacity: 0.35;
    }
    div.stButton > button p {
        font-size: 1.35rem !important;
        font-weight: 900 !important;
    }

    .board-frame {
        background-color: #1a4494;
        border: 3px solid #102a5c;
        border-radius: 10px;
        padding: 16px;
        margin: 8px auto 20px auto;
    }
    .board-row {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 12px;
        margin-bottom: 12px;
    }
    .board-row:last-child {
        margin-bottom: 0;
    }
    .slot {
        aspect-ratio: 1 / 1;
        border-radius: 50%;
        background-color: #0d1117;
        border: 3px solid #102a5c;
    }
    .slot-clickable {
        cursor: pointer;
    }
    .slot-col-hover {
        border-color: #9ca3af !important;
    }
    .slot-human {
        background-color: #e63946;
        border: 3px solid #9e1b26;
    }
    .slot-ai {
        background-color: #ffb703;
        border: 3px solid #b57c00;
    }
    .slot-win {
        border: 4px solid #ffffff !important;
    }

    .last-move-bar {
        font-size: 1.3rem;
        font-weight: 800;
        color: #f0f6fc;
        padding-top: 9px;
        text-transform: uppercase;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title-text">Four in a Row</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="legend-box">
        <div class="legend-item">
            <span class="disc-icon disc-red"></span>
            <span>RED: PLAYER</span>
        </div>
        <div class="legend-item">
            <span class="disc-icon disc-yellow"></span>
            <span>YELLOW: AI</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if game.game_over:
    if game.winner == HUMAN:
        st.markdown('<div class="result-box">PLAYER WINS</div>', unsafe_allow_html=True)
    elif game.winner == AI:
        st.markdown('<div class="result-box">AI WINS</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-box">DRAW</div>', unsafe_allow_html=True)

cols = st.columns(COLS)
for c in range(COLS):
    with cols[c]:
        playable = (
            not game.game_over
            and game.current_turn == HUMAN
            and game.is_valid_col(game.board, c)
        )
        if st.button(
            str(c + 1),
            key=f"col_btn_{c}",
            disabled=not playable,
            use_container_width=True,
        ):
            if game.play_human_move(c):
                st.rerun()

win_set = set(game.winning_coords)
html = '<div class="board-frame">'
for r in range(ROWS - 1, -1, -1):
    html += '<div class="board-row">'
    for c in range(COLS):
        val = game.board[r][c]
        if val == HUMAN:
            cls = "slot slot-human"
        elif val == AI:
            cls = "slot slot-ai"
        else:
            cls = "slot"

        if (
            not game.game_over
            and game.current_turn == HUMAN
            and game.is_valid_col(game.board, c)
        ):
            cls += " slot-clickable"

        if (r, c) in win_set:
            cls += " slot-win"

        html += f'<div class="{cls}" data-col="{c}"></div>'
    html += "</div>"
html += "</div>"

st.markdown(html, unsafe_allow_html=True)

components.html(
    """
    <script>
    const doc = window.parent.document;

    if (window.parent._c4Click) {
        doc.removeEventListener('click', window.parent._c4Click);
        doc.removeEventListener('mouseover', window.parent._c4Over);
        doc.removeEventListener('mouseout', window.parent._c4Out);
    }

    window.parent._c4Click = function(e) {
        const slot = e.target.closest('.slot-clickable[data-col]');
        if (!slot) return;
        const col = parseInt(slot.getAttribute('data-col'), 10);
        const label = String(col + 1);
        const buttons = doc.querySelectorAll('button');
        for (const b of buttons) {
            if (b.innerText.trim() === label && !b.disabled) {
                b.click();
                break;
            }
        }
    };

    window.parent._c4Over = function(e) {
        const slot = e.target.closest('.slot-clickable[data-col]');
        if (!slot) return;
        const col = slot.getAttribute('data-col');
        doc.querySelectorAll(`.slot-clickable[data-col="${col}"]`).forEach(el => {
            el.classList.add('slot-col-hover');
        });
    };

    window.parent._c4Out = function(e) {
        const slot = e.target.closest('.slot-clickable[data-col]');
        if (!slot) return;
        const col = slot.getAttribute('data-col');
        doc.querySelectorAll(`.slot-clickable[data-col="${col}"]`).forEach(el => {
            el.classList.remove('slot-col-hover');
        });
    };

    doc.addEventListener('click', window.parent._c4Click);
    doc.addEventListener('mouseover', window.parent._c4Over);
    doc.addEventListener('mouseout', window.parent._c4Out);
    </script>
    """,
    height=0,
)

if not game.game_over and game.current_turn == AI:
    game.play_ai_move()
    st.rerun()

left, right = st.columns([1.3, 2.7])
with left:
    if st.button("NEW GAME", use_container_width=True):
        game.reset()
        st.rerun()

with right:
    if game.move_history:
        p, r, c = game.move_history[-1]
        who = "PLAYER" if p == HUMAN else "AI"
        st.markdown(
            f'<div class="last-move-bar">LAST MOVE: {who} (COL {c + 1})</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="last-move-bar">LAST MOVE: NONE</div>',
            unsafe_allow_html=True,
        )