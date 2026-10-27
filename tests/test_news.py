import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import blue_posts


class News(unittest.TestCase):
    def test_foreign_and_unverified_records_cannot_enter_snapshot(self):
        p={'id':1,'classifier_version':1,'kind':'forever','title':'News','posted':'2026-10-27T00:00:00Z','checked_at':'2026-10-27T00:00:00Z','url':'https://us.forums.blizzard.com/en/wow/t/news/1'}
        self.assertTrue(blue_posts.valid_post(p))
        self.assertFalse(blue_posts.valid_post({**p,'kind':'unverified'}))
        self.assertFalse(blue_posts.valid_post({**p,'url':'https://evil.example/t/1'}))
        self.assertFalse(blue_posts.valid_post({**p,'url':'https://evil@us.forums.blizzard.com/en/wow/t/1'}))

    def test_failed_refresh_retains_success_time_but_drops_unverified_legacy(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'blue.json'
            old={'fetched':'2026-10-25T00:00:00Z','posts':[{'id':1,'title':'Old unclassified post'}]}
            path.write_text(json.dumps(old))
            with patch.object(blue_posts,'read',side_effect=OSError('offline')):
                result=blue_posts.refresh(path)
            data=json.loads(path.read_text())
            self.assertEqual(data['fetched'],old['fetched'])
            self.assertEqual(data['posts'],[])
            self.assertEqual(data['status'],'unavailable')
            self.assertIsNotNone(result['error'])

    def test_successful_full_text_can_remove_a_now_unrelated_cached_post(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'blue.json'
            p={'id':1,'topic_id':1,'category_id':347,'topic_title':'Forever update','url':'/t/news/1/1','created_at':'2026-10-27T00:00:00Z','username':'Blizzard'}
            old={'id':1,'classifier_version':1,'kind':'forever','title':'Forever update','posted':p['created_at'],'checked_at':p['created_at'],'url':blue_posts.FORUM+p['url']}
            path.write_text(json.dumps({'fetched':p['created_at'],'posts':[old]}))
            article={'id':1,'html':'<p>Entirely unrelated article content for another subject with enough text.</p>','title':'Other news','posted':p['created_at'],'url':old['url'],'category_id':1,'author':'Blizzard','reply':False}
            with patch.object(blue_posts,'read',side_effect=[json.dumps({'posts':[p]}),json.dumps({'posts':[]})]),patch.object(blue_posts,'inspect',return_value=article):
                blue_posts.refresh(path)
            self.assertEqual(json.loads(path.read_text())['posts'],[])

if __name__=='__main__':unittest.main()
