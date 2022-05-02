import { useState } from "react";
import { Button, View, Text, TextInput } from "react-native";
import axios from "axios";
export default function Login({ navigation }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onSubmit = async () => {
    console.log("email: ", email);
    console.log("password: ", password);

    try {
      const response = await axios.post("http://localhost:5000/register", {
        email,
        password,
      });
      if (response.status === 200) {
        navigation.navigate("login");
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      console.log("error: ", error);
    }
  };

  return (
    <View
      style={{
        padding: "1rem",
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        rowGap: "1rem",
      }}
    >
      <View
        style={{
          width: "50rem",
          display: "flex",
          rowGap: "2rem",
        }}
      >
        <Text
          style={{ fontSize: "2rem", fontWeight: "bold", marginBottom: "1rem" }}
        >
          Sign Up
        </Text>
        <View style={{ display: "flex", rowGap: "1rem" }}>
          <View style={{ display: "flex" }}>
            <Text>Email</Text>
            <TextInput
              onChangeText={(text) => setEmail(text)}
              style={{ backgroundColor: "lightgray", padding: "0.5rem" }}
              placeholder="example@mail.com"
            />
          </View>
          <View style={{ display: "flex" }}>
            <Text>Password</Text>
            <TextInput
              onChangeText={(text) => setPassword(text)}
              style={{
                backgroundColor: "lightgray",
                padding: "0.5rem",
                letterSpacing: "0.5rem",
              }}
              placeholder="********"
            />
          </View>
          <Button color="#20B2AA" title="Sign Up" onPress={onSubmit} />
        </View>
        <Button
          color="#4682B4"
          onPress={() => navigation.navigate("login")}
          title="Log in"
        />
      </View>
    </View>
  );
}
