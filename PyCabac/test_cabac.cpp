#include <cstdint>
#include <iostream>
#include <tuple>
#include <utility>
#include <vector>

#include "bin_decoder.h"
#include "bin_encoder.h"
#include "bitstream.h"
#include <fstream>

using namespace std;

void main() {

    {
        std::cout << "--- test_encodeBin" << std::endl;

        std::ifstream t("E:\\git_repo\\adaptive-mixing\\PyCabac\\text.txt");
        std::stringstream buffer;
        buffer << t.rdbuf();
        
        string inpString = buffer.str();
        
        
        cabacEncoder encX, encY, mixEnc;
        std::vector<std::tuple<double, uint8_t>> ctxInit;

        for (int i = 0; i < 8;i++) {
            ctxInit.push_back({ 0.5, i});
        }
 
        encX.initCtx(ctxInit);
        encX.start();
        encY.initCtx(ctxInit);
        encY.start();
        mixEnc.initCtx(ctxInit);
        mixEnc.start();

        vector<unsigned> inpBits;
        for (auto it = inpString.begin(); it < inpString.end(); it++) {
            unsigned bit = (*it) & 0x01;
            inpBits.push_back(bit);

            bit = ((*it) & 0x02) >> 1;
            inpBits.push_back(bit);

            bit = ((*it) & 0x04) >> 2;
            inpBits.push_back(bit);

            bit = ((*it) & 0x08) >> 3;
            inpBits.push_back(bit);

            bit = ((*it) & 0x10) >> 4;
            inpBits.push_back(bit);

            bit = ((*it) & 0x20) >> 5;
            inpBits.push_back(bit);

            bit = ((*it) & 0x40) >> 6;
            inpBits.push_back(bit);

            bit = ((*it) & 0x80) >> 7;
            inpBits.push_back(bit);
        }


        int64_t context = 0;
        unsigned contextMask = 0x03;
        for (auto it = inpBits.begin(); it < inpBits.end(); it++) {
            unsigned bit = *it;
            encX.encodeBin(bit, 0);
            encY.encodeBin(bit, context);

            auto encXLen = encX.getBitstream().size();
            auto encYLen = encY.getBitstream().size();
            double encXWeight = (encYLen) / (encXLen + encYLen);

            auto mixedContext = encX.m_Ctx[context & contextXMask];
            context=(context << 1 | bit)& contextMask;
        }

        
        encX.encodeBinTrm(1);
        encX.finish();
        encX.writeByteAlignment();

        encY.encodeBinTrm(1);
        encY.finish();
        encY.writeByteAlignment();

        std::vector<uint8_t> byteVector = encX.getBitstream();
        cout << "encX output length: " << byteVector.size() << endl;
        byteVector = encY.getBitstream();
        cout << "encY output length: " << byteVector.size() << endl;

        cabacDecoder binDecoder(byteVector);
        binDecoder.initCtx(ctxInit);
        binDecoder.start();
        std::cout << "Decoded bin: " << binDecoder.decodeBin(0) << std::endl;
        std::cout << "Decoded bin: " << binDecoder.decodeBin(0) << std::endl;

        binDecoder.finish();
    }

}