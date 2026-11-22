import streamlit as st
import random
import time

st.set_page_config(page_title="Tic-Tac-Toe", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    max-width: 650px;
}

div[class*="st-key-cell_"] button {
    aspect-ratio: 1 / 1;
    height: auto !important;
    width: 100%;
    padding: 0 !important;
    border-radius: 10px !important;
    display: flex;
    align-items: center;
    justify-content: center;
}

div[class*="st-key-cell_"] button,
div[class*="st-key-cell_"] button p,
div[class*="st-key-cell_"] button span {
    font-size: 4.5rem !important;
    font-weight: 800 !important;
    line-height: 1 !important;
    margin: 0 !important;
}

div[class*="st-key-cell_"] button:disabled {
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; margin-bottom: 0.5rem;'>Tic-Tac-Toe</h2>", unsafe_allow_html=True)

if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.draws = 0
    st.session_state.game_over = False
    st.session_state.waiting_for_ai = False
    st.session_state.message = "Your turn. You are X."

winning_combinations = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def check_winner(board):
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a]:
            return board[a]
    return None


def minimax(board, maximizing):
    winner = check_winner(board)

    if winner == "O":
        return 1
    if winner == "X":
        return -1
    if "" not in board:
        return 0

    scores = []

    for i in range(9):
        if board[i] == "":
            board[i] = "O" if maximizing else "X"
            scores.append(minimax(board, not maximizing))
            board[i] = ""

    return max(scores) if maximizing else min(scores)


def ai_move(board):
    available = [i for i in range(9) if board[i] == ""]

    if not available:
        return

    if random.random() < 0.4:
        move = random.choice(available)
    else:
        best_score = float("-inf")
        move = available[0]

        for i in available:
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""

            if score > best_score:
                best_score = score
                move = i

    board[move] = "O"


def end_game(result):
    st.session_state.game_over = True

    if result == "X":
        st.session_state.wins += 1
        st.session_state.message = "You won!"

    elif result == "O":
        st.session_state.losses += 1
        st.session_state.message = "The computer won."

    else:
        st.session_state.draws += 1
        st.session_state.message = "It's a draw."


def player_move(position):
    board = st.session_state.board

    if st.session_state.game_over or board[position] != "":
        return

    board[position] = "X"

    winner = check_winner(board)

    if winner:
        end_game(winner)
        return

    if "" not in board:
        end_game(None)
        return

    st.session_state.waiting_for_ai = True


total = st.session_state.wins + st.session_state.losses + st.session_state.draws
win_rate = st.session_state.wins / total * 100 if total > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Wins", st.session_state.wins)
col2.metric("Losses", st.session_state.losses)
col3.metric("Draws", st.session_state.draws)
col4.metric("Win Rate", f"{win_rate:.0f}%")

st.markdown(f"<p style='text-align: center; font-weight: bold;'>{st.session_state.message}</p>", unsafe_allow_html=True)

_, board_col, _ = st.columns([0.15, 0.7, 0.15])

with board_col:
    for row in range(3):
        columns = st.columns(3)

        for col in range(3):
            position = row * 3 + col
            value = st.session_state.board[position]

            if value == "X":
                label = ":blue[X]"
            elif value == "O":
                label = ":red[O]"
            else:
                label = " "

            with columns[col]:
                st.button(
                    label,
                    key=f"cell_{position}",
                    use_container_width=True,
                    disabled=(
                        st.session_state.game_over
                        or value != ""
                        or st.session_state.waiting_for_ai
                    ),
                    on_click=player_move,
                    args=(position,)
                )

if st.session_state.waiting_for_ai:
    with st.spinner("Computer is thinking..."):
        time.sleep(0.5)
        ai_move(st.session_state.board)

    winner = check_winner(st.session_state.board)

    if winner:
        end_game(winner)
    elif "" not in st.session_state.board:
        end_game(None)
    else:
        st.session_state.message = "Your turn. You are X."

    st.session_state.waiting_for_ai = False
    st.rerun()

_, btn_col, _ = st.columns([0.15, 0.7, 0.15])
with btn_col:
    b1, b2 = st.columns(2)
    with b1:
        if st.button("New Game", use_container_width=True):
            st.session_state.board = [""] * 9
            st.session_state.game_over = False
            st.session_state.waiting_for_ai = False
            st.session_state.message = "Your turn. You are X."
            st.rerun()

    with b2:
        if st.button("Reset Statistics", use_container_width=True):
            st.session_state.wins = 0
            st.session_state.losses = 0
            st.session_state.draws = 0
            st.rerun()
