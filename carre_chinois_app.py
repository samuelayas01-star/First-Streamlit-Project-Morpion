import streamlit as st
import numpy as np


st.header("Carré Chinois")
#Pour recommencer tout le jeu
def reset_variables():
    st.session_state.board = np.full((3, 3), "")
    st.session_state.player = "X"
    st.session_state.game_over = False
    st.session_state.selected_piece = None
    st.session_state.phase = "placement"    #placement revient à mouvement
    st.rerun()
if "board" not in st.session_state:
    reset_variables()
#Fonction pour compter le nombre de pions
def count_pieces(symbol: str) -> int:
    return int(np.sum(st.session_state.board == symbol))

#pour changer de pion
def change_player()-> None:
    st.session_state.player = "O" if st.session_state.player == "X" else "X"

#Changer de joueur en fonction du pion
def player_name()-> str:
    if st.session_state.player == "X":
        return "Joueur A"
    else:
        return "Joueur B"
st.write(f"Joueur actuel : {player_name()}")

#Création de la fonction qui vérifie qui a gagné
def check_winner(M)-> bool:
    for i in range(3):
        if all(M[i, :] == M[i, 0]) and M[i, 0] != "":
            return True
        if all(M[:, i] == M[0, i]) and M[0, i] != "":
            return True
    if all(np.diag(M) == M[0, 0]) and M[0, 0] != "":
        return True
    if all(np.diag(np.fliplr(M)) == M[0, 2]) and M[0, 2] != "":
        return True
    return False

# Dictionnaire des voisins autorisés (déplacements le long des lignes)
ADJACENCY = {
    (0, 0): {(0, 1), (1, 0), (1, 1)},
    (0, 1): {(0, 0), (0, 2), (1, 1)},
    (0, 2): {(0, 1), (1, 2), (1, 1)},
    (1, 0): {(0, 0), (2, 0), (1, 1)},
    (1, 1): {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    },
    (1, 2): {(0, 2), (2, 2), (1, 1)},
    (2, 0): {(1, 0), (2, 1), (1, 1)},
    (2, 1): {(2, 0), (2, 2), (1, 1)},
    (2, 2): {(1, 2), (2, 1), (1, 1)},
}

#Fonction pour valider le deplacement d'un pion
def validate_movement(source: tuple[int, int], dst: tuple[int, int])-> bool:
    if dst not in ADJACENCY[source]:
        return False
    if st.session_state.board[dst[0]][dst[1]] != "":
        return False
    return True

#
def on_cell_click(i: int, j: int) -> None:
    if st.session_state.game_over:
        return None
    board = st.session_state.board
    player = st.session_state.player
    
    #Phase de placement des pions
    if st.session_state.phase == "placement":
        if board[i][j] == "" and count_pieces(player) < 3:
            board[i][j] = player
            if check_winner(board) == True:
                st.session_state.game_over = True
            else:
                change_player()
        if count_pieces("X") == 3 and count_pieces("O") == 3:
            st.session_state.phase = "movement"
    if st.session_state.phase == "movement":
        selected = st.session_state.selected_piece
        if selected is None:
            if board[i][j] == player:
                st.session_state.selected_piece = (i, j)
                return None
            
        if board[i][j] == player:
            st.session_state.selected_piece = (i, j)
            return None
        if validate_movement(selected, (i, j)) == True:
            board[selected[0]][selected[1]] = ""
            board[i][j] = player
            if check_winner(board) == True:
                st.session_state.game_over = True
                st.session_state.selected_piece = None
            else:
                change_player()
    st.rerun()
# Création de la grille
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        if cols[j].button(st.session_state.board[i][j] or " ", key=f"{i}{j}"):
            on_cell_click(i, j)
    
#Dialogue du vainqueur
if st.session_state.game_over == True:
    @st.dialog("Vainqueur 🎉")
    def show_dialog():
        st.success(f"🎊 {player_name()} a gagné !")
        #Boutton pour recommencer le jeu
        col1, col2 = st.columns(2)
        with col1:
            left1, center1, rigth1 = st.columns([1, 2, 1])
            with center1:
                Restart = st.button("Restart", width="stretch")
        with col2:
            left2, center2, right2 = st.columns([1, 2, 1])
            with center2:
                Quitter = st.button("Quit", width="stretch")
        if Restart:
            reset_variables()
        if Quitter:
            st.warning('Vous pouvez fermer cet onglet')
    show_dialog()
# Affichage tableau
st.write("Plateau actuel :")
st.write(st.session_state.board)

#Boutton pour recommencer le jeu
Restart = st.button("Reprendre le jeu")
if Restart:
    reset_variables()