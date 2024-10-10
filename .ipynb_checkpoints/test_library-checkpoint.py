import unittest
import tempfile
import json

# toto je vase reseni
import solution

test_data = {
    "books": [
        {
            "title": "The Silent Valley",
            "author": "Mary Brown",
            "isbn": "978-1028-5853-2"
        },
        {
            "title": "Mysteries of the Cosmos",
            "author": "Robert Lopez",
            "isbn": "978-6782-6252-8"
        },
        {
            "title": "Journey Through Time",
            "author": "Patricia Moore",
            "isbn": "978-2954-6542-8"
        },
    ],
    "magazines": [
        {
            "title": "Global Explorer",
            "volume": 85,
            "issue_number": 8
        },
        {
            "title": "Tech Today",
            "volume": 41,
            "issue_number": 5
        },
        {
            "title": "Modern Artist",
            "volume": 52,
            "issue_number": 3
        },
    ]
}


class TestItems(unittest.TestCase):
    def test_inheritance_book(self):
        self.assertTrue(issubclass(solution.Book, solution.Item))

    def test_inheritance_magazine(self):
        self.assertTrue(issubclass(solution.Magazine, solution.Item))

    def test_attributes_book(self):
        book = solution.Book("kniha", "vaclav", 1234567890)
        self.assertTrue(hasattr(book, "author"))
        self.assertTrue(hasattr(book, "isbn"))

    def test_attributes_magazine(self):
        magazine = solution.Magazine("casopis", 20, 10)
        self.assertTrue(hasattr(magazine, "volume"))
        self.assertTrue(hasattr(magazine, "issue_number"))


class TestLibrary(unittest.TestCase):
    def setUp(self) -> None:
        self.test_set = [
            solution.Book(title='The Silent Valley', author='Mary Brown', isbn='978-1028-5853-2'),
            solution.Book(title='Mysteries of the Cosmos', author='Robert Lopez', isbn='978-6782-6252-8'),
            solution.Book(title='Journey Through Time', author='Patricia Moore', isbn='978-2954-6542-8'),
            solution.Magazine(title='Global Explorer', volume=85, issue_number=8),
            solution.Magazine(title='Tech Today', volume=41, issue_number=5),
            solution.Magazine(title='Modern Artist', volume=52, issue_number=3),
        ]

        self.lib = solution.Library()
        for item in self.test_set:
            self.lib.add_item(item)

    def test_books(self):
        books = self.lib.get_books()
        self.assertTrue(all(isinstance(x, solution.Book) for x in books))

    def test_magazines(self):
        magazines = self.lib.get_magazines()
        self.assertTrue(all(isinstance(x, solution.Magazine) for x in magazines))

    def test_iter(self):
        items = list(self.lib)
        self.assertListEqual(items, self.test_set)

    def test_iter_stop(self):
        with self.assertRaises(StopIteration):
            it = iter(self.lib)
            while True:
                next(it)

    def test_checkout(self):
        book = self.test_set[0]
        self.lib.checkout(book.title)

    def test_not_found(self):
        with self.assertRaises(solution.ItemNotFoundError):
            self.lib.checkout("tahle kniha neexistuje")

    def test_not_available(self):
        with self.assertRaises(solution.ItemNotAvailableError):
            book = self.test_set[0]
            self.lib.checkout(book.title)
            self.lib.checkout(book.title)

    def test_checked_out(self):
        with self.assertRaises(solution.ItemNotCheckedOutError):
            book = self.test_set[0]
            self.lib.return_item(book.title)

    def test_load_from_file(self):
        with tempfile.NamedTemporaryFile("wt", delete=False) as file:
            json.dump(test_data, file)
            file.close()

            lib = solution.Library.load_from_file(file.name)
        try:
            lib.checkout(test_data["books"][0]["title"])
        except:
            self.fail("lookup should not fail now")
