from sklearn.model_selection import train_test_split
import numpy as np 
from tensorflow.keras import optimizers, callbacks
from Models import build_model_1, build_model_2

model = build_model_2()
model.compile(optimizer=optimizers.Adam(1e-3),
              loss='mean_squared_error')
model.summary()

X = np.load("npys/X.npy")
X = X.reshape((X.shape[0], X.shape[2], X.shape[3], X.shape[1]))
Y = np.load("npys/Y.npy")
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.15, random_state=42)

np.save("npys/X_test.npy", X_test)
np.save("npys/Y_test.npy", Y_test)

# early_stoppings = callbacks.EarlyStopping('val_loss', patience=15)
checkpoint_callback = callbacks.ModelCheckpoint(
    filepath="model_2",  # File path to save the model
    monitor='val_loss',  # Metric to monitor (e.g., validation loss)
    save_best_only=True,  # Save only the best model (based on the monitored metric)
    mode='min',  # Mode can be 'min' (for loss) or 'max' (for accuracy)
    save_weights_only=False,  # Save the entire model (including architecture)
    verbose=1  # Display messages about checkpoint saving
)

model.fit(X_train, Y_train,
          batch_size=8,
          epochs=300,
          verbose=1,
          validation_split=0.2,
          callbacks=[
                    # early_stoppings,
                     checkpoint_callback])
