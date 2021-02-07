from NetMaker import BATCH_SIZE, NetMaker
from State import State
from Serializer import serialize_state
from random import choices
import os
import tensorflow as tf

SAVE_PATH = "C:/Users/Cosmo/Documents/GitHub/moradin-ai/savedmodel"
CHECKPOINT_PATH = "training_7/cp.ckpt"
CHECKPOINT_DIR = os.path.dirname(CHECKPOINT_PATH)
NUM_TRAINING_GAMES = 500

def fit_stage(x_train, y_train):
    # Create a callback that saves the model's weights
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=CHECKPOINT_PATH,
                                                     save_weights_only=True,
                                                     verbose=1,
                                                     save_best_only=False)

    try:
        model.load_weights(CHECKPOINT_PATH)
    except Exception:
        print("first time!")

    print("Fit model on training data:")
    history = model.fit(
        x_train,
        y_train,
        batch_size=BATCH_SIZE,
        epochs=30,
        # We pass some validation for
        # monitoring validation loss and metrics
        # at the end of each epoch
        callbacks=[cp_callback]
    )

    model.save(SAVE_PATH)


def sample_probabilities(p, game: State):
    moves = list(range(9))
    move = choices(moves, p)[0]
    while move not in game.legal_moves():
        move = choices(moves, p)[0]
    return move

def run_training_match(model):
    stateMoveDict = dict()
    stateValueDict = dict()
    game = State()
    while game.is_game_over() == False:
        probabilities = model(serialize_state(game))
        stateMoveDict[serialize_state(game)] = probabilities
        move = sample_probabilities(probabilities, game)
        game.play(move)
    probabilities = model(serialize_state(game))
    stateMoveDict[serialize_state(game)] = probabilities
    return stateMoveDict

if __name__ == "__main__":
    model = NetMaker()()
    
    for n in range(NUM_TRAINING_GAMES):
        stateMoveDict = run_training_match(model)
