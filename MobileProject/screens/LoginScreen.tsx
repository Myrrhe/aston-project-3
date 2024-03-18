import React, { useState } from 'react';
import { StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';

const LoginScreen = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const onPressLogin = async () => {
        console.log(email, password);

        let csrf = '';

        try {
            const response = await fetch('http://127.0.0.1:8000/get-csrf', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    // Cookie: 'csrftoken=RiakuA2GJwEIgvkmFK65sBr8bYRLKi5K',
                },
                // credentials: 'include',
            });

            if (!response.ok) {
                throw new Error('CSRF token not gotten');
            }
            console.log('CSRF token gotten');
            console.log(response);
          } catch (error : any) {
            console.error('CSRF token not gotten :', error.message);
            console.error(error);
        }

        // try {
        //     const response = await fetch('http://127.0.0.1:8000/fr/login/', {
        //         method: 'POST',
        //         headers: {
        //             'Content-Type': 'application/json',
        //         },
        //         body: JSON.stringify({
        //             username: email,
        //             password,
        //         }),
        //     });

        //     if (!response.ok) {
        //         console.log(response);
        //         throw new Error('Erreur lors de la connexion123456');
        //     }

        //     // Gérer la réponse ici, par exemple, afficher un message de succès ou rediriger l'utilisateur
        //     console.log('Connecté avec succès');
        //   } catch (error : any) {
        //     console.error('Erreur lors de la connexion :', error.message);
        //     // Gérer l'erreur, par exemple, afficher un message d'erreur à l'utilisateur
        // }
    };

    const onPressForgotPassword = () => {
        // Do something about forgot password operation
    };

    const onPressSignUp = () => {

    };

    return (
        <View style={styles.container}>
            <View style={styles.container}>
                <Text style={styles.title}>Login Screen</Text>
            </View>
            <View style={styles.inputView}>
                <TextInput
                    style={styles.inputText}
                    placeholder='Email'
                    placeholderTextColor='#003f5c'
                    onChangeText={text => setEmail(text)} />
            </View>
            <View style={styles.inputView}>
                <TextInput
                    style={styles.inputText}
                    secureTextEntry
                    placeholder="Password"
                    placeholderTextColor="#003f5c"
                    onChangeText={text => setPassword(text)} />
            </View>

            <TouchableOpacity
                onPress={onPressForgotPassword}>
                <Text style={styles.forgotAndSignUpText}>Forgot Password?</Text>
            </TouchableOpacity>
            <TouchableOpacity
                onPress={onPressLogin}style={styles.loginBtn}>
                <Text style={styles.forgotAndSignUpText}>LOGIN</Text>
            </TouchableOpacity>
            <TouchableOpacity
                onPress={onPressSignUp}>
                <Text style={styles.inputText}>Signup</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    input: {
        height: 40,
        borderColor: 'gray',
        borderWidth: 1,
        marginBottom: 10,
        paddingHorizontal: 10,
    },
    title: {
        fontWeight: 'bold',
        fontSize: 50,
        color: '#fb5b5a',
        marginBottom: 40,
    },
    inputView: {
        width: '80%',
        backgroundColor: '#3AB4BA',
        borderRadius: 25,
        height: 50,
        marginBottom: 20,
        justifyContent: 'center',
        padding: 20,
    },
    inputText: {
        height: 50,
        color: 'white',
    },
    forgotAndSignUpText: {
        color: 'white',
        fontSize: 11,
    },
    loginBtn: {
        width: '80%',
        backgroundColor: '#fb5b5a',
        borderRadius: 25,
        height: 50,
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 40,
        marginBottom: 10,
    },
});

export default LoginScreen;
