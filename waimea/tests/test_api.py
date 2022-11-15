import unittest
import json
from api import app, gen_filename

class TestAPIMethods(unittest.TestCase):

    app.testing=True

    def test_log(self):
        with app.log() as client:
            sent = {"25"}
            result = client.post("/log", data=sent)
            self.assertEqual(result.data, json.dumps(sent))

    # TODO: break up api.py into methods that can be unit tested (e.g. write to log file)

    def test_file_name_formatter(self):
        base_name = "./logs/wave_heights"
        suffix = "20-18"
        extension = "csv"
        result = gen_filename(base_name=base_name, suffix=suffix, extension=extension)
        self.assertEqual(result, "wave_heights_20-18.csv")




if __name__ == '__main__':
    unittest.main()