from PySide6.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def init_stats_tab(self):
        layout = QVBoxLayout()
        self.stats_tab.setLayout(layout)

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)
        self.update_stats()

    def update_stats(self):
        self.canvas.figure.clf()
        ax = self.canvas.figure.add_subplot(111)
        watched = [m.rating for m in self.user.movies if m.status.lower() == "watched" and m.rating is not None]
        labels = [m.title for m in self.user.movies if m.status.lower() == "watched" and m.rating is not None]

        if watched:
            ax.bar(labels, watched, color='skyblue')
            ax.set_title("Oceny obejrzanych filmów")
            ax.set_ylabel("Ocena")
            ax.set_ylim(0, 10)
            ax.set_xticklabels(labels, rotation=45, ha='right')
        else:
            ax.text(0.5, 0.5, "Brak danych do wyświetlenia", ha='center', va='center')

        self.canvas.draw()