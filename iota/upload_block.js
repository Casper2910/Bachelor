"use strict";
// Copyright 2021-2023 IOTA Stiftung
// SPDX-License-Identifier: Apache-2.0
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var sdk_1 = require("@iota/sdk");
require('dotenv').config({ path: '.env' });
// Run with command:
// yarn run-example ./client/08-data-block.ts
// In this example we will send a block with a tagged data payload.
function run() {
    return __awaiter(this, void 0, void 0, function () {
        var _i, _a, envVar, client, options, mnemonic, secretManager, blockIdAndBlock, fetchedBlock, payload, error_1;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    (0, sdk_1.initLogger)();
                    for (_i = 0, _a = ['NODE_URL', 'EXPLORER_URL']; _i < _a.length; _i++) {
                        envVar = _a[_i];
                        if (!(envVar in process.env)) {
                            throw new Error(".env ".concat(envVar, " is undefined, see .env.example"));
                        }
                    }
                    client = new sdk_1.Client({
                        // Insert your node URL in the .env.
                        nodes: [process.env.NODE_URL],
                    });
                    options = {
                        tag: (0, sdk_1.utf8ToHex)('Hello'),
                        data: (0, sdk_1.utf8ToHex)('Tangle'),
                    };
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 4, , 5]);
                    mnemonic = sdk_1.Utils.generateMnemonic();
                    secretManager = { mnemonic: mnemonic };
                    return [4 /*yield*/, client.buildAndPostBlock(secretManager, options)];
                case 2:
                    blockIdAndBlock = _b.sent();
                    console.log("Block sent: ".concat(process.env.EXPLORER_URL, "/block/").concat(blockIdAndBlock[0]));
                    return [4 /*yield*/, client.getBlock(blockIdAndBlock[0])];
                case 3:
                    fetchedBlock = _b.sent();
                    console.log('Block data: ', fetchedBlock);
                    if (fetchedBlock.payload instanceof sdk_1.TaggedDataPayload) {
                        payload = fetchedBlock.payload;
                        console.log('Decoded data:', (0, sdk_1.hexToUtf8)(payload.data));
                    }
                    return [3 /*break*/, 5];
                case 4:
                    error_1 = _b.sent();
                    console.error('Error: ', error_1);
                    return [3 /*break*/, 5];
                case 5: return [2 /*return*/];
            }
        });
    });
}
run().then(function () { return process.exit(); });
