import { combineReducers, configureStore } from '@reduxjs/toolkit'
import userReducer from "./user/userSlice";
import  { persistReducer, persistStore } from 'redux-persist'
import storage  from 'redux-persist/lib/storage'
import notificationSlice from './notification/notificationSlice';

const rootReducer =  combineReducers ({
  user: userReducer,
  notification: notificationSlice,
  
})
const persistConfig = {
  key: 'root',
  storage,
  verion: 1,
}
const persistedReducer = persistReducer(persistConfig, rootReducer)

export const store = configureStore({
 
    reducer: persistedReducer,
    middleware: (getDefaultMiddleware) => getDefaultMiddleware({
      serializableCheck: false,
    }),
  
})

export const persistor = persistStore(store)