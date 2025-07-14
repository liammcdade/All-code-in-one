import tkinter as tk
from tkinter import messagebox

# Card ranks and suits
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['♠', '♥', '♦', '♣']

def all_cards():
    return [r + s for r in RANKS for s in SUITS]

class PokerSolverGUI:
    def __init__(self, master):
        self.master = master
        master.title("Texas Hold'em Poker Solver")

        self.selected_cards = []
        self.card_buttons = []

        tk.Label(master, text="Select Your Hand (2 cards):").pack()
        self.hand_frame = tk.Frame(master)
        self.hand_frame.pack()
        self.hand_vars = [tk.StringVar() for _ in range(2)]
        for i in range(2):
            opt = tk.OptionMenu(self.hand_frame, self.hand_vars[i], *all_cards())
            opt.pack(side=tk.LEFT)

        tk.Label(master, text="Select Community Cards (up to 5):").pack()
        self.comm_frame = tk.Frame(master)
        self.comm_frame.pack()
        self.comm_vars = [tk.StringVar() for _ in range(5)]
        for i in range(5):
            opt = tk.OptionMenu(self.comm_frame, self.comm_vars[i], *([''] + all_cards()))
            opt.pack(side=tk.LEFT)

        # Add ante, blinds, and starting chips inputs
        tk.Label(master, text="Ante:").pack()
        self.ante_var = tk.IntVar(value=0)
        tk.Entry(master, textvariable=self.ante_var).pack()

        tk.Label(master, text="Small Blind:").pack()
        self.sb_var = tk.IntVar(value=10)
        tk.Entry(master, textvariable=self.sb_var).pack()

        tk.Label(master, text="Big Blind:").pack()
        self.bb_var = tk.IntVar(value=20)
        tk.Entry(master, textvariable=self.bb_var).pack()

        tk.Label(master, text="Starting Chips:").pack()
        self.chips_var = tk.IntVar(value=1000)
        tk.Entry(master, textvariable=self.chips_var).pack()

        self.sim_btn = tk.Button(master, text="Simulate & Advise", command=self.simulate)
        self.sim_btn.pack(pady=10)

        self.progress_label = tk.Label(master, text="Progress: 0%")
        self.progress_label.pack()

        self.result_label = tk.Label(master, text="Advice will appear here.")
        self.result_label.pack()

    def simulate(self):
        hand = [v.get() for v in self.hand_vars]
        comm = [v.get() for v in self.comm_vars if v.get()]
        all_selected = set(hand + comm)
        if len(all_selected) != len(hand) + len(comm):
            self.result_label.config(text="Duplicate cards selected!")
            return
        if '' in hand or any(h not in all_cards() for h in hand):
            self.result_label.config(text="Please select 2 valid hand cards.")
            return
        ante = self.ante_var.get()
        sb = self.sb_var.get()
        bb = self.bb_var.get()
        chips = self.chips_var.get()
        # Simulate all possible remaining cards for the board
        total_sims = 10000
        for i in range(total_sims):
            percent = int((i + 1) / total_sims * 100)
            self.progress_label.config(text=f"Progress: {percent}%")
            self.master.update_idletasks()
            # Here you would run a real simulation for each scenario
        advice = self.simple_advice(hand, comm)
        advice += f"\nAnte: {ante}, Small Blind: {sb}, Big Blind: {bb}, Starting Chips: {chips}"
        self.result_label.config(text=advice)

    def simple_advice(self, hand, comm):
        # Placeholder: always says 'Check/Fold' unless you have a pair
        ranks = [c[0] for c in hand + comm]
        for r in set(ranks):
            if ranks.count(r) >= 2:
                return "You have a pair! Consider betting."
        return "No strong hand detected. Check or fold."

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerSolverGUI(root)
    root.mainloop()
