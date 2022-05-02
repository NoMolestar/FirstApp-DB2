export const initialState = {
  email: "",
  password: "",
};

const GlobalReducer = (state, action) => {
  switch (action.type) {
    case "LOGIN": {
      return {
        ...state,
        email: action.email,
        password: action.password,
      };
    }
    case "LOGOUT": {
      return { ...state, ...initialState };
    }
    default:
      return state;
  }
};

export default GlobalReducer;
