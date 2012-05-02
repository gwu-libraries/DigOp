from django.template import Library, Node
from ui.models import Book
from ui.models import ProcessingSession

register = Library()

class Barcodes(Node):
    def render(self, context):
		books = Book.objects.all()
		barcodes = []
		for book in books:
			barcodes.append(book.barcode)
		context['barcodes'] = barcodes
		return ''


def get_all_barcodes(parser, token):
    return Barcodes()

#get_all_barcodes = register.tag(get_all_barcodes)
register.tag('get_all_barcodes', get_all_barcodes)
