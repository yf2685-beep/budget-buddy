"""Record Budget Buddy against an isolated, in-memory demo database."""
from datetime import datetime
import mongomock
import pymongo
from demo_capture import DEMO_TIME, Recorder, browser_session, load, options


def main():
    args = options(__file__, 'budget-workflow.gif')
    db_client = mongomock.MongoClient()
    pymongo.MongoClient = lambda *a, **k: db_client
    module = load('budget_demo_app', args.root / 'app.py')
    app = module.app
    db = db_client.portfolio_demo
    db.monthly_budgets.insert_one({'budget': 1200.0, 'month': 11, 'year': 2026,
                                  'notes': 'Fictional student budget', 'created_at': DEMO_TIME})
    for day, amount, category, note in [(2, 280, 'Rent', 'Shared apartment'),
                                       (5, 48, 'Groceries', 'Weekly groceries'),
                                       (12, 15, 'Transit', 'Metro card'),
                                       (17, 22, 'Food', 'Lunch with classmates')]:
        db.expenses.insert_one({'date': datetime(2026, 11, day), 'year': 2026, 'month': 11,
                                'amount': amount, 'category': category, 'note': note, 'title': category})
    with browser_session(app, args) as (_, page, base):
        rec = Recorder(page, 'Budget Buddy', 'Actual Flask pages / isolated in-memory database')
        page.goto(base, wait_until='networkidle')
        page.locator('#mb-content').wait_for(state='visible')
        rec.snap('01 / Review the monthly budget', 1600)
        page.goto(base + '/expense_new', wait_until='networkidle')
        page.locator('input[name=date]').fill('2026-11-20')
        rec.snap('02 / Record a new expense', 600)
        rec.type('input[name=amount]', '12.50', '02 / Record a new expense', chunks=3)
        rec.type('input[name=category]', 'Food', '02 / Record a new expense', chunks=3)
        rec.type('textarea[name=note]', 'Coffee and a sandwich', '02 / Record a new expense')
        rec.click('button[type=submit]', '02 / Save the expense')
        page.wait_for_url('**/expenses_list')
        page.wait_for_load_state('networkidle')
        assert db.expenses.count_documents({'note': 'Coffee and a sandwich'}) == 1
        rec.snap('03 / Find the saved expense', 1000)
        rec.type('input[name=category]', 'Food', '03 / Filter spending by category', chunks=3)
        rec.click('button[type=submit]', '03 / Filter spending by category')
        page.wait_for_load_state('networkidle')
        assert 'Coffee and a sandwich' in page.locator('body').inner_text()
        assert 'category=Food' in page.url
        assert 'Shared apartment' not in page.locator('body').inner_text()
        rec.snap('03 / Filter spending by category', 1500)
        page.goto(base, wait_until='networkidle')
        page.wait_for_function("document.querySelector('#mb-spent').textContent === '377.50'")
        rec.snap('04 / Review the updated total', 1900)
        rec.save(args.output)
    print('Verified: expense persisted, filter rendered, total updated to 377.50')


if __name__ == '__main__':
    main()
