# Ten Pin Bowling ScoreCard

## Hubbub Technical Test

### Installation:
pip install -r requirements.txt

### Run the tests
nosetests tests

The Warning message in the output is expected.

### Playing the the file locally
python3
from src.ScoreCard import ScoreCard
sc = ScoreCard()
sc.bowl(10)

