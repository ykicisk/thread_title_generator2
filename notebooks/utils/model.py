import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Embedding, Activation, \
    BatchNormalization, GRU, Bidirectional


def create_rnn_generator_model(gru_units, embedding_dim, vocab_size, num_stacks=4):
    input_y = Input(shape=(1, ))  # 1文字ずつ処理する
    before_state_list = []
    for _ in range(num_stacks):
        before_state_list.append(Input(shape=(gru_units, )))

    x = Embedding(input_dim=vocab_size, output_dim=embedding_dim)(input_y)  # (batch, 1, embedding_dim)

    next_state_list = []
    for idx, before_state in enumerate(before_state_list):
        x, next_state = GRU(gru_units,
                return_sequences=idx<len(before_state_list)-1,  # 最後だけretrun_sequencesしない
                return_state=True, recurrent_initializer='glorot_uniform')(x, initial_state=before_state)
        next_state_list.append(next_state)

    x = Dense(vocab_size)(x)  # (None, vocab_size)

    return Model(inputs=[input_y] + before_state_list, outputs=[x] + next_state_list)


def create_generation_evaluator_model(base_embedding_layer, gen_units, embedding_dim, seq_len, vocab_size):
    input_y = Input(shape=(seq_len, ))

    embedding_layer = Embedding(input_dim=vocab_size, output_dim=embedding_dim)
    x = embedding_layer(input_y)  # (batch, seq_len, embedding_dim)

    x = Bidirectional(
            GRU(gen_units,  # dropout=0.5, recurrent_dropout=0.5,
                return_sequences=True, recurrent_initializer='glorot_uniform'))(x)
    x = Bidirectional(
            GRU(gen_units,  #  dropout=0.25, recurrent_dropout=0.0,
                recurrent_initializer='glorot_uniform'))(x)
    x = Dense(gen_units)(x)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)
    x = Dense(1)(x)

    model = Model(inputs=input_y, outputs=x)

    embedding_weights = [var.numpy() for var in base_embedding_layer.weights]
    embedding_layer.set_weights(embedding_weights)
    embedding_layer.trainable = False
 
    return model

