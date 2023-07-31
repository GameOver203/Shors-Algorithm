namespace shors {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Math;

    
    operation PhaseEstimation(
        x : Int,
        N : Int,
        precision : Int) : Int 
    {
        // create superposition of eigenvectors by creating qubits encoding number 1
        let eigenLength = Floor(Lg(IntAsDouble(N)))+1;
        use eigenvec = Qubit[eigenLength];
        X(eigenvec[0]);

        // create register which will ultimately store approximation of s/r.
        use register = Qubit[precision];
        ApplyToEachA(H, register);

        // apply controlled Uj operator
        ControlledUj(x, N, register, eigenvec);

        // apply quantum fourier transform inverse to obtain approximation of s/r
        Adjoint QFT (BigEndian(register));

       // convert register into integer representing (approximation of s/r)*2^(precision) for continued fraction algorithm to be applied later
        mutable result = 0;
        for i in 0..precision-1 {
            set result = 2 * result;
            if M(register[i]) == One {
                set result = result + 1;
            }
        }
        ResetAll(eigenvec);
        ResetAll(register);
        return result;
    }

    // applies controlled Uj operator
    operation ControlledUj(
        x : Int,
        N : Int,
        register : Qubit[],
        eigenvector : Qubit[]) : Unit
    {
        let length = Length(register);

        mutable power = 1;
        for i in 0..length-1 {
            Controlled ConstructU ([register[length - 1 - i]], (x, N, power, eigenvector));
            set power = 2 * power;
        }
    }

    // computes the Unitary transform we need
    operation ConstructU(
        x : Int, 
        modulus : Int, 
        power : Int, 
        target : Qubit[]) : Unit is Adj + Ctl {
    // 
        MultiplyByModularInteger(FastPowerMod(x, power, modulus), modulus, LittleEndian(target));
    }

    // computes modulo power of number efficiently
    function FastPowerMod (
        x : Int,
        power : Int,
        modulus : Int) : Int 
    {
        mutable times = x;
        mutable result = 1;
        mutable powerBits = power;

        let powerLength = BitSizeI(power);
        for i in 0..powerLength-1 {
            if powerBits % 2 == 1 {
                set result = (times * result) % modulus;
            }
            set times = (times * times) % modulus;
            set powerBits = powerBits / 2;
        }
        return result % modulus;
    }
}

