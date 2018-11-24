# Ten Pin Bowling ScoreCard

## Hubbub Technical Test

### Installation:
pip install -r requirements.txt

### Run the tests
```nosetests tests``` 

The Warning message in the output is expected.

### Playing with the file locally
```python3```  
```from src.ScoreCard import ScoreCard```  
```sc = ScoreCard()```  
```sc.bowl(10)```  
```sc.bowl(2)```  
```sc.bowl(6)```  
```sc.bowl(-4)```  
```sc.bowl("10")```  
```sc.bowl(2)```  
```sc.bowl(8)```  
```sc.get_game_state()```
