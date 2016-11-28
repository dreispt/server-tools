# -*- coding: utf-8 -*-
# © 2016 Daniel Reis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
from openerp import SUPERUSER_ID


# Extended name search is only used on some operators
ALLOWED_OPS = set(['ilike', 'like'])


def _extend_name_results(self, domain, results, limit):
    result_count = len(results)
    if result_count < limit:
        domain += [('id', 'not in', [x[0] for x in results])]
        recs = self.search(domain, limit=limit - result_count)
        results.extend(recs.name_get())
    return results


class ModelExtended(models.Model):
    _inherit = 'ir.model'

    def _register_hook(self, cr, ids=None):

        def make_search():

            def search(self, cr, user, args, offset=0, limit=None, order=None, context=None, count=False):
                new_args = expand_domain(args)
                # Perform standard name search
                res = search.origin(
                    self, cr, user, args, offset, limit, order, context, count)
                enabled = self.env.context.get('name_search_extended', True)
                # Perform extended name search
                # Note: Empty name causes error on
                #       Customer->More->Portal Access Management
                if name and enabled and operator in ALLOWED_OPS:
                    # Support a list of fields to search on
                    all_names = _get_rec_names(self)
                    base_domain = args or []
                    # Try regular search on each additional search field
                    for rec_name in all_names[1:]:
                        domain = [(rec_name, operator, name)]
                        res = _extend_name_results(
                            self, base_domain + domain, res, limit)
                    # Try ordered word search on each of the search fields
                    for rec_name in all_names:
                        domain = [(rec_name, operator, name.replace(' ', '%'))]
                        res = _extend_name_results(
                            self, base_domain + domain, res, limit)
                    # Try unordered word search on each of the search fields
                    for rec_name in all_names:
                        domain = [(rec_name, operator, x)
                                  for x in name.split() if x]
                        res = _extend_name_results(
                            self, base_domain + domain, res, limit)
                return res
            return name_search

        if ids is None:
            ids = self.search(cr, SUPERUSER_ID, [])
        for model in self.browse(cr, SUPERUSER_ID, ids):
            Model = self.pool.get(model.model)
            if Model:
                Model._patch_method('search', make_search())
        return super(ModelExtended, self)._register_hook(cr)
