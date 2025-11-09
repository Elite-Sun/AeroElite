import { configureStore } from '@reduxjs/toolkit';
import uiReducer from './slices/uiSlice';
import authReducer from './slices/authSlice';
import designReducer from './slices/designSlice';

export const store = configureStore({
  reducer: {
    ui: uiReducer,
    auth: authReducer,
    design: designReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
