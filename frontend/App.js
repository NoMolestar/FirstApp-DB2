import * as React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Home from "./pages/Home";
import Details from "./pages/Details";
import Login from "./pages/Login";
import Info from "./pages/Info";
import Signup from "./pages/Signup";
import GlobalContext from "./utils/GlobalContext";
import GlobalReducer, { initialState } from "./utils/GlobalReducer";

const Stack = createNativeStackNavigator();

export default function App() {
  const [state, dispatch] = React.useReducer(GlobalReducer, initialState);
  return (
    <GlobalContext.Provider value={{ state, dispatch }}>
      <NavigationContainer linking={{ enabled: true }}>
        <Stack.Navigator
          initialRouteName="login"
          screenOptions={{ headerShown: false }}
        >
          <Stack.Screen name="login" component={Login} />
          <Stack.Screen name="home" component={Home} />
          <Stack.Screen name="details" component={Details} />
          <Stack.Screen name="info" component={Info} />
          <Stack.Screen name="signup" component={Signup} />
        </Stack.Navigator>
      </NavigationContainer>
    </GlobalContext.Provider>
  );
}
