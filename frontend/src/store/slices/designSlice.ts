import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Design {
  id: number;
  name: string;
  component_type: string;
  parameters: any;
  cad_file_path?: string;
  thumbnail_path?: string;
}

interface DesignState {
  currentDesign: Design | null;
  designs: Design[];
  loading: boolean;
  validationResults: any;
}

const initialState: DesignState = {
  currentDesign: null,
  designs: [],
  loading: false,
  validationResults: null,
};

const designSlice = createSlice({
  name: 'design',
  initialState,
  reducers: {
    setCurrentDesign: (state, action: PayloadAction<Design>) => {
      state.currentDesign = action.payload;
    },
    setDesigns: (state, action: PayloadAction<Design[]>) => {
      state.designs = action.payload;
    },
    addDesign: (state, action: PayloadAction<Design>) => {
      state.designs.push(action.payload);
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setValidationResults: (state, action: PayloadAction<any>) => {
      state.validationResults = action.payload;
    },
  },
});

export const { setCurrentDesign, setDesigns, addDesign, setLoading, setValidationResults } =
  designSlice.actions;
export default designSlice.reducer;
