# -*- coding: utf-8 -*-
# © 2016 Daniel Reis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp import SUPERUSER_ID


class FieldExtended(models.Model):
    _inherit = 'ir.model.fields'
    is_name_searched = fields.Boolean()


class ModelExtended(models.Model):
    _inherit = 'ir.model'

    name_search_ids = fields.One2many(
        'ir.model.fields',
        'model_id',
        domain=[('is_name_searched', '=', True)],
        readonly=True)

    def _search_extend_leaf(self, leaf):
        if len(leaf) == 1:
            return [leaf]
        # fuzzy search: search for all the words; pipe is a valid separator
        if leaf[1] == 'ilike' and self.context.get('search_fuzzy_enabled'):
            field = leaf[0]
            values = leaf[2].split()
            new_leaf = list()
            for value in values:
                new_leaf.extend(['&', (field, 'ilike', value)])
            del new_leaf[-1]
        else:
            new_leaf = [leaf]
        return new_leaf

    def _search_extend(self, domain):
        new_domain = list()
        for leaf in domain:
            new_domain.extend(self._search_extend_leaf(leaf))
        return new_domain

    def _register_hook(self, cr, ids=None):

        def make_name_search():
            @api.model
            def name_search(self, name='', args=None,
                            operator='ilike', limit=100):
                print "name_Search", name, args, self.env.context
                res = name_search.origin(self, name, args, operator, limit)
                if not res and ' ' in name.strip() and self._rec_name:
                    # Support a list of fields to search on
                    rec_names = (
                        getattr(self, '_rec_search') or [self._rec_name])
                    # Try ordered word search
                    for rec_name in rec_names:
                        domain = [(self._rec_name, operator,
                                   name.replace(' ', '%'))]
                        recs = self.search(domain, limit=limit)
                        if recs:
                            return recs.name_get()
                    # Unordered word search
                    for rec_name in rec_names:
                        domain = [(self._rec_name, operator, x)
                                  for x in name.split() if x]
                        recs = self.search(domain, limit=limit)
                        if recs:
                            return recs.name_get()
                return res
            return name_search

        def make_search():
            @api.returns(
                'self',
                upgrade=lambda self, value, args, offset=0, limit=None,
                order=None,
                count=False: value if count else self.browse(value),
                downgrade=lambda self, value, args, offset=0, limit=None,
                order=None, count=False: value if count else value.ids)
            def search(self, cr, user, args, offset=0, limit=None,
                       order=None, context=None, count=False):
                SearchExtend = self.env['base.search.extend']
                new_domain = SearchExtend._search_extend(self, args),
                return search.origin(
                    self, cr, user, new_domain, offset, limit,
                    order, context, count)
            return search

        if ids is None:
            ids = self.search(cr, SUPERUSER_ID, [])
        for model in self.browse(cr, SUPERUSER_ID, ids):
            Model = self.pool[model.model]
            Model._rec_search = model.name_search_id.mapped('name')
            print Model, Model._rec_search
            Model._patch_method('name_search', make_name_search())
        return super(ModelExtended, self)._register_hook(cr, ids=ids)
