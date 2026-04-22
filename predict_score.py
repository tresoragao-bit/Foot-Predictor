# Prédicteur de score exact de football basé sur les 5 derniers résultats

import argparse
import sys
import tkinter as tk
from collections import Counter
from tkinter import messagebox
from typing import List, Tuple


def parse_score(score: str) -> Tuple[int, int]:
    """Parse un score de la forme '2-1' et retourne (buts_dom, buts_ext)."""
    try:
        home, away = score.strip().split("-")
        return int(home), int(away)
    except ValueError as err:
        raise ValueError(f"Score invalide : '{score}'. Utilisez le format X-Y.") from err


def predict_exact_score(previous_scores: List[str]) -> str:
    """Prédit un score exact à partir des 5 derniers scores.

    previous_scores doit contenir 5 scores sous la forme '2-1'.
    La fonction utilise un mélange de fréquence et de moyenne pondérée des buts.
    """
    if len(previous_scores) != 5:
        raise ValueError("Il faut fournir exactement 5 scores précédents.")

    parsed = [parse_score(score) for score in previous_scores]

    most_common = Counter(previous_scores).most_common(1)
    if most_common and most_common[0][1] > 1:
        return most_common[0][0]

    weights = [1.0, 1.2, 1.4, 1.6, 2.0]
    total_home = 0.0
    total_away = 0.0
    total_weight = 0.0

    for (home, away), weight in zip(parsed, weights):
        total_home += home * weight
        total_away += away * weight
        total_weight += weight

    avg_home = total_home / total_weight
    avg_away = total_away / total_weight

    predicted_home = max(0, round(avg_home))
    predicted_away = max(0, round(avg_away))

    return f"{predicted_home}-{predicted_away}"


def predict_from_input(entries: List[tk.Entry], result_label: tk.Label) -> None:
    scores = [entry.get().strip() for entry in entries]
    try:
        prediction = predict_exact_score(scores)
        result_label.config(text=f"Prédiction : {prediction}")
    except ValueError as err:
        messagebox.showerror("Erreur de saisie", str(err))


def create_gui() -> None:
    root = tk.Tk()
    root.title("Prédicteur de score de foot")
    root.geometry("380x320")
    root.resizable(False, False)

    tk.Label(root, text="Entrez les 5 derniers scores (format X-Y)", font=("Arial", 12, "bold")).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(padx=20)

    entries = []
    for i in range(5):
        row = tk.Frame(frame)
        row.pack(fill="x", pady=4)
        label = tk.Label(row, text=f"Match {i + 1}", width=10, anchor="w")
        label.pack(side="left")
        entry = tk.Entry(row, width=20)
        entry.pack(side="left", padx=8)
        entries.append(entry)

    result_label = tk.Label(root, text="Prédiction : -", font=("Arial", 12))
    result_label.pack(pady=14)

    button = tk.Button(
        root,
        text="Prédire",
        width=18,
        command=lambda: predict_from_input(entries, result_label),
    )
    button.pack(pady=6)

    tk.Label(
        root,
        text="Exemple : 1-0 2-1 1-1 2-0 1-2",
        font=("Arial", 9),
        fg="gray",
    ).pack(pady=8)

    root.mainloop()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prédit un score exact de football à partir des 5 derniers scores.")
    parser.add_argument(
        "scores",
        nargs="*",
        help="Cinq scores précédents au format X-Y, par exemple 1-0 2-1 1-1 2-0 1-2.")
    parser.add_argument(
        "--example",
        action="store_true",
        help="Affiche un exemple d'utilisation avec des scores fictifs.")
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Ouvre une interface graphique pour saisir les scores.")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    if args.gui:
        create_gui()
        return

    if args.example:
        derniers_scores = ["1-0", "2-1", "1-1", "2-0", "1-2"]
    else:
        if len(args.scores) != 5:
            print(
                "Erreur : il faut fournir exactement 5 scores précédents au format X-Y.",
                file=sys.stderr,
            )
            print("Exemple : python predict_score.py 1-0 2-1 1-1 2-0 1-2", file=sys.stderr)
            print("Pour ouvrir l'interface graphique : python predict_score.py --gui", file=sys.stderr)
            sys.exit(1)
        derniers_scores = args.scores

    try:
        prediction = predict_exact_score(derniers_scores)
    except ValueError as err:
        print(f"Erreur : {err}", file=sys.stderr)
        sys.exit(1)

    print("Scores précédents :", derniers_scores)
    print("Prédiction du score exact :", prediction)


if __name__ == "__main__":
    main()
