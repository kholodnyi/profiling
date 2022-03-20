import datetime

import matplotlib.pyplot as plt
from matplotlib import ticker
from prettytable import PrettyTable


class BSTNode:
    def __init__(self, val=None):
        self.left = None
        self.right = None
        self.val = val

    def insert(self, val):
        if not self.val:
            self.val = val
            return

        if self.val == val:
            return

        if val < self.val:
            if self.left:
                self.left.insert(val)
                return
            self.left = BSTNode(val)
            return

        if self.right:
            self.right.insert(val)
            return
        self.right = BSTNode(val)

    def get_min(self):
        current = self
        while current.left is not None:
            current = current.left
        return current.val

    def get_max(self):
        current = self
        while current.right is not None:
            current = current.right
        return current.val

    def delete(self, val):
        if self is None:
            return self
        if val < self.val:
            if self.left:
                self.left = self.left.delete(val)
            return self
        if val > self.val:
            if self.right:
                self.right = self.right.delete(val)
            return self
        if self.right is None:
            return self.left
        if self.left is None:
            return self.right
        min_larger_node = self.right
        while min_larger_node.left:
            min_larger_node = min_larger_node.left
        self.val = min_larger_node.val
        self.right = self.right.delete(min_larger_node.val)
        return self

    def exists(self, val):
        if val == self.val:
            return True

        if val < self.val:
            if self.left is None:
                return False
            return self.left.exists(val)

        if self.right is None:
            return False
        return self.right.exists(val)

    def preorder(self, vals):
        if self.val is not None:
            vals.append(self.val)
        if self.left is not None:
            self.left.preorder(vals)
        if self.right is not None:
            self.right.preorder(vals)
        return vals

    def inorder(self, vals):
        if self.left is not None:
            self.left.inorder(vals)
        if self.val is not None:
            vals.append(self.val)
        if self.right is not None:
            self.right.inorder(vals)
        return vals

    def postorder(self, vals):
        if self.left is not None:
            self.left.postorder(vals)
        if self.right is not None:
            self.right.postorder(vals)
        if self.val is not None:
            vals.append(self.val)
        return vals


def plot_time_results(results: dict, filename: str):
    fig, ax = plt.subplots(3)  # Create a figure containing a single axes.
    fig.set_figheight(12)
    fig.set_figwidth(12)
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.4)

    ax[0].plot(results.keys(), [val['insert'] for val in results.values()], label='insert')
    ax[0].set_xscale('log')
    ax[0].set_title('Insert')
    ax[0].set_xlabel('BST size')
    ax[0].set_ylabel('Execution time (s)')

    ax[1].plot(results.keys(), [val['search'] for val in results.values()], label='search')
    ax[1].set_xscale('log')
    ax[1].set_title('Search')
    ax[1].set_xlabel('BST size')
    ax[1].set_ylabel('Execution time (s)')

    ax[2].plot(results.keys(), [val['delete'] for val in results.values()], label='delete')
    ax[2].set_xscale('log')
    ax[2].set_title('Delete')
    ax[2].set_xlabel('BST size')
    ax[2].set_ylabel('Execution time (s)')

    plt.savefig(filename, format='png')


def plot_memory_results(results: dict, filename: str):
    fig, ax = plt.subplots(1)  # Create a figure containing a single axes.
    fig.set_figheight(5)
    fig.set_figwidth(12)
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.4)

    ax.plot(results.keys(), [val['memory'] / 1048576 for val in results.values()], label='space')
    ax.set_title('Memory consumption')
    ax.set_xlabel('BST size')
    ax.set_ylabel('Size (MB)')

    ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    ax.ticklabel_format(style='plain')
    plt.savefig(filename, format='png')


def print_table(headers: list, results: list, align: str = None) -> None:
    x = PrettyTable()
    x.field_names = headers

    for data_row in results:
        x.add_row(data_row)

    if align:
        for i, align_char in enumerate(align):
            x.align[headers[i]] = align_char
    print(x)


def to_timedelta(s):
    return datetime.timedelta(seconds=s)
