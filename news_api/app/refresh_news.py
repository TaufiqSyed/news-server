# Every day at 1am, fetch data from the News API

from datetime import datetime
from news_api.app.models import NewsArticle
from news_api.app.repositories import NewsArticleRepository
from django_cron import CronJobBase, Schedule

class refresh_news(CronJobBase):
    RUN_EVERY_MINS = 1 # 1440 every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'news_api.refresh_news'    # a unique code

    def do(self):
        print('cron job...')
        try:
            last_article = NewsArticle.objects.order_by("publishedAt")[-1:].get()
            from_ = latest_date = last_article.publishedAt.isoformat()
            print('from found')
        except IndexError:
            from_ = datetime(1970, 1, 1).isoformat()
            print('from set to epoch')
        print('attempting api call')
        articles = NewsArticleRepository.getNewsArticles({
            'from': latest_date.isoformat(),
            'sortBy': 'publishedDate'
        })
        print(articles)
    # NewsArticle.objects.bulk_create(articles)