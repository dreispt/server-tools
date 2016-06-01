# -*- coding: utf-8 -*-
# © 2016 Daniel Reis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class SomethingCase(TransactionCase):

    def setUp(self):
        self.Partner = self.env['res.partner']
        # Johann Gambolputty  https://www.youtube.com/watch?v=UDPqB9i1ScY
        self.partner1 = self.Partner.create(
            {'name': 'Johann Gambolputty de von Ausfern Hautkopft of Ulm'})

    def test_FuzzySearchDisabledByDefault(self):
        """Fuzzy search is disabled by default"""
        res = self.Partner.search(
            [('name', 'ilike', 'ausfern haut johann')])
        self.assertFalse(res)

    def test_FuzzyMatchesContainingWords(self):
        """Fuzzy search finds matches containing the words"""
        res = self.Partner.with_context(search_fuzzy_enabled=True).search(
            [('name', 'ilike', 'ausfern haut johann')])
        self.assertTrue(res)

    def test_FuzzyMatchesMustContaininAllWords(self):
        """Fuzzy search matches must contain all words"""
        res = self.Partner.with_context(search_fuzzy_enabled=True).search(
            [('name', 'ilike', 'ausfern haut johann eric')])
        self.assertFalse(res)
