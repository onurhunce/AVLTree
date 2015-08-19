import random
import unittest


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class AVLTree:
    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0

    def get_height(self):
        if self.node:
            return self.node.height
        else:
            return 0

    def insert(self, key):
        """
        Insert nodes to the tree.
        """
        tree = self.node
        new_node = Node(key)

        if tree is None:
            self.node = new_node
            self.node.left = AVLTree()
            self.node.right = AVLTree()

        elif key < tree.key:
            self.node.left.insert(key)

        elif key > tree.key:
            self.node.right.insert(key)

        self.re_balance_tree()

    def re_balance_tree(self):
        """
        Rebalanced the tree if it is unbalanced.
        """

        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.rotate_left()
                    self.update_heights()
                    self.update_balances()
                self.rotate_right()
                self.update_heights()
                self.update_balances()

            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rotate_right()
                    self.update_heights()
                    self.update_balances()
                self.rotate_left()
                self.update_heights()
                self.update_balances()

    def rotate_right(self):
        root = self.node
        left_child = self.node.left.node
        right_child = left_child.right.node

        self.node = left_child
        left_child.right.node = root
        root.left.node = right_child

    def rotate_left(self):
        root = self.node
        right_child = self.node.right.node
        left_child = right_child.left.node

        self.node = right_child
        right_child.left.node = root
        root.right.node = left_child

    def update_heights(self, recurse=True):
        if not self.node is None:
            if recurse:
                if self.node.left is not None:
                    self.node.left.update_heights()
                if self.node.right is not None:
                    self.node.right.update_heights()

            self.height = max(self.node.left.height,
                              self.node.right.height) + 1
        else:
            self.height = -1

    def update_balances(self, recurse=True):
        if not self.node is None:
            if recurse:
                if self.node.left is not None:
                    self.node.left.update_balances()
                if self.node.right is not None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0

    def check_balanced(self):
        if self is None or self.node is None:
            return True

        self.update_heights()
        self.update_balances()
        return ((abs(
            self.balance) < 2) and self.node.left.check_balanced() and
                self.node.right.check_balanced())

    def print_tree_in_order_traversal(self):
        if self.node is None:
            return []
        nodes_list = []
        l = self.node.left.print_tree_in_order_traversal()
        for i in l:
            nodes_list.append(i)

        nodes_list.append(self.node.key)

        l = self.node.right.print_tree_in_order_traversal()
        for i in l:
            nodes_list.append(i)

        return nodes_list

    def print_tree_as_tree_shape(self, node=None, level=0):
        if not node:
            node = self.node

        if node.right.node:
            self.print_tree_as_tree_shape(node.right.node, level + 1)
            print ('\t' * level), (' / ')
        print ('\t' * level), node.key

        if node.left.node:
            print ('\t' * level), (' \\ ')
            self.print_tree_as_tree_shape(node.left.node, level + 1)


def create_random_node_list():
    # Create random list for node values.
    random_node_list = random.sample(range(1, 100), 10)
    print "Input :", random_node_list, "\n"
    return random_node_list


def create_avl_tree(node_list):
    # Create tree and insert node values.
    tree = AVLTree()
    for node in node_list:
        tree.insert(node)
    return tree


class AvlTreeTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.Tree = AVLTree()

    def test_rotate_right_function(self):
        self.Tree.insert(8)
        self.Tree.insert(5)
        self.Tree.insert(4)
        print"\n"
        print "-Testing rotate right function- inserted values with order:8, " \
              "5, 4 "
        self.Tree.print_tree_as_tree_shape()
        print "-----------------------------"
        self.assertEqual(self.Tree.node.key, 5)

    def test_rotate_left_function(self):
        self.Tree.insert(4)
        self.Tree.insert(6)
        self.Tree.insert(8)
        print"\n"
        print "-Testing rotate left function- inserted values with order:4, " \
              "6, 8 "
        self.Tree.print_tree_as_tree_shape()
        print "-----------------------------"
        self.assertEqual(self.Tree.node.key, 6)

    def test_rotate_left_right_possibility(self):
        self.Tree.insert(10)
        self.Tree.insert(5)
        self.Tree.insert(7)
        print"\n"
        print "-Testing rotate left-right possibility- inserted values with " \
              "order:10, 5, 7"
        self.Tree.print_tree_as_tree_shape()
        print "-----------------------------"
        self.assertEqual(self.Tree.node.key, 7)

    def test_rotate_right_left_possibility(self):
        self.Tree.insert(6)
        self.Tree.insert(12)
        self.Tree.insert(9)
        print"\n"
        print "-Testing rotate right-left possibility- inserted values with " \
              "order:6, 12, 9"
        self.Tree.print_tree_as_tree_shape()
        print "-----------------------------"
        self.assertEqual(self.Tree.node.key, 9)

    def test_empty_tree_get_height_function(self):
        empty_tree_height = self.Tree.get_height()
        self.assertEqual(empty_tree_height, 0)

    def test_tree_with_big_amount_of_node_elements(self):
        random_node_list = random.sample(range(1, 1000000), 100000)
        test_tree = create_avl_tree(random_node_list)
        self.assertTrue(test_tree.node is not None)
        print "  --Tree is tested with 100000 node elements and pass the " \
              "test.-- "
        print "    Total spending time for this test is written below."

if __name__ == "__main__":
    unittest.main()
    avl_tree = create_avl_tree(create_random_node_list())
    avl_tree.print_tree_as_tree_shape()
