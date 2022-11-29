from nonogram import Nonogram

nonogram_6_9 = Nonogram(
    left_constraints=[
        [5, 1],
        [6, 1],
        [3, 1, 2],
        [1, 1, 3],
        [5],
        [3, 1, 1]
    ],
    top_constraints=[
        [2, 1], [6], [3, 2], [2, 2], [3, 1], [2, 2], [1, 1], [1, 2], [2, 1]
    ]
)

nonogram_14_10 = Nonogram(
    left_constraints=[
        [2, 2],
        [3, 2],
        [2, 3],
        [1, 4],
        [2, 5],
        [3, 5],
        [10],
        [10],
        [9],
        [7],
        [5],
        [3],
        [1, 1],
        [4]
    ],
    top_constraints=[
        [1, 2],
        [3, 5],
        [10],
        [6, 1],
        [8],
        [9, 1],
        [12],
        [10],
        [10],
        [1, 5]
    ]
)

nonogram_6_9.solve()
nonogram_14_10.solve()